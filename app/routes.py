from app import app
from flask import render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
import os
import time
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
# Initialise the LoginManager
login_manager.init_app(app)
# If login_required, redirect back to /login
login_manager.login_view = 'login'

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "info.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)

import app.models as models  # need 'db' to import models
from app.forms import Add_Club, Add_Teacher, Club_Teacher, Remove_Admin, Add_Notice, Add_Event, Add_Photo, Remove_Club, Remove_Teacher, Update_Club, SearchClubForm, LoginForm, SignupForm, Add_Admin


@login_manager.user_loader
def load_user(user_id):
    # Gets primary key value and then uses primary key value to find user sql_alchemy instance
    return models.User.query.filter_by(id=user_id).first()


@app.route("/")
def home():
    club_photos = [club.pro_photo for club in models.Clubs.query.all()]
    return render_template("home.html", title="Home Page", club_photos=club_photos)


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if user with the same email is already in the database
        user_check = models.User.query.filter_by(email=form.email.data).first()
        if not user_check:
            # Create new user instance
            user = models.User()
            # Assign form values to instance attributes
            picture = form.picture.data
            filename = secure_filename(picture.filename)
            user.picture = ('static/images/' + filename)
            picture.save(os.path.join(basedir, 'static/images/' + filename))
            user.name = form.name.data
            user.email = form.email.data
            user.password = generate_password_hash(form.password.data, salt_length=16)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash("A User with the same email already exists!")
        return redirect(url_for('signup'))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Checks if user with input email exists
        user_info = models.User.query.filter_by(email=form.email.data).first()
        # If exists, check db hash with input password and if there's a match, login user
        if user_info:
            if check_password_hash(user_info.password, form.password.data):
                login_user(user_info, remember=True)
                return redirect(url_for("home"))
            else:
                flash("Username Or Password is incorrect!")
        else:
            flash("User Does Not Exist!")
        return redirect(url_for('login'))
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return render_template("home.html", title="Logout")


@app.route("/clubs", methods=["GET", "POST"])
def clubs():
    form = SearchClubForm()
    clubs = []
    club_status = {}

    if form.validate_on_submit() and 'search_query' in request.form:
        search_query = form.search_query.data
        clubs = models.Clubs.query.filter(models.Clubs.name.like(f"%{search_query}%")).all()
        if not clubs:
            flash("No Results", "info")
    elif request.method == "POST" and 'add_favorite' in request.form:
        club_id = request.form.get('add_favorite')
        club = models.Clubs.query.get(club_id)
        if current_user not in club.User:
            club.User.append(current_user)
            db.session.commit()
            flash(f"Added {club.name} to your favorites!")
        else:
            flash(f"You're already a member of {club.name}!")
        return redirect(url_for('clubs'))
    else:
        clubs = models.Clubs.query.all()

    if current_user.is_authenticated:
        club_status = {club.id: current_user in club.User for club in clubs}
    else:
        # If not authenticated, all clubs are not favorited
        club_status = {club.id: False for club in clubs}

    return render_template("clubs.html", title="Clubs Page", clubs=clubs, form=form, club_status=club_status)


@app.route("/club/<int:id>")
def club(id):
    club = models.Clubs.query.filter_by(id=id).first()

    return render_template('club.html', club=club)


@app.route("/teach/<int:id>")
@login_required
def teacher(id):
    teacher = models.Teachers.query.filter_by(id=id).first() 
    if not teacher:
        # Teacher not found, return 404
        abort(404)

    if teacher.email != current_user.email:
        # Current user email does not match the teacher's email, return 404
        abort(404)
    return render_template("teacher.html", title="Teacher Club Access",
                           teacher=teacher)


@app.route("/user/<int:id>", methods=['GET', 'POST'])
def user(id):
    user = models.User.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template("dashboard.html", title="User Club Access ",
                            user=user)
    else:
        # Handle removing a favourite
        if 'remove_favourite' in request.form:
            club_id = request.form.get('remove_favourite')
            favourite_to_remove = models.Clubs.query.filter_by(id=club_id).first()
            if favourite_to_remove:
                user.clubs.remove(favourite_to_remove)
                db.session.commit()
                flash('Favourite Removed!')
            return redirect(f"/user/{id}")


@app.route("/club_admin/<int:id>", methods=['GET', 'POST'])
def club_admin(id):

    club_admin = models.Clubs.query.filter_by(id=id).first()
    notice_form = Add_Notice()
    event_form = Add_Event()
    photo_form = Add_Photo()
    update_form = Update_Club()
    if request.method == 'GET':
        return render_template('club_admin.html',
                               title="Club Admin Access Page",
                               notice_form=notice_form, club_admin=club_admin,
                               event_form=event_form, photo_form=photo_form,
                               update_form=update_form)
    else:
        # Handle deleting a notice
        if 'delete_notice' in request.form:
            notice_id = request.form.get('delete_notice')
            notice_to_delete = models.Notices.query.filter_by(id=notice_id).first()
            if notice_to_delete:
                club_admin.notices.remove(notice_to_delete)
                db.session.commit()
                flash('Notice Deleted!')
            return redirect(f"/club_admin/{id}")

        # Handle deleting an event
        if 'delete_event' in request.form:
            event_id = request.form.get('delete_event')
            event_to_delete = models.Events.query.filter_by(id=event_id).first()
            if event_to_delete:
                club_admin.events.remove(event_to_delete)
                db.session.commit()
                flash('Event Deleted!')
            return redirect(f"/club_admin/{id}")

        if notice_form.validate_on_submit():
            new_notice = models.Notices()
            new_notice.notice = notice_form.notice.data
            new_notice.date = notice_form.date.data
            photo = notice_form.photo.data
            filename = secure_filename(photo.filename)
            new_notice.photo = ('static/images/' + filename)
            photo.save(os.path.join(basedir, 'static/images/' + filename))
            club_admin.notices.append(new_notice)
            db.session.commit()
            flash('Notice Added!')
            time.sleep(2.5)
            return redirect(f"/club_admin/{id}")

        if event_form.validate_on_submit():
            new_event = models.Events()
            new_event.name = event_form.name.data
            new_event.date = event_form.date.data
            photo = event_form.photo.data
            filename = secure_filename(photo.filename)
            new_event.photo = ('static/images/' + filename)
            photo.save(os.path.join(basedir, 'static/images/' + filename))
            club_admin.events.append(new_event)
            db.session.commit()
            flash('Event Added!')
            time.sleep(2.5)
            return redirect(f"/club_admin/{id}")

        if photo_form.validate_on_submit():
            new_photo = models.Photos()
            photo = photo_form.photo.data
            filename = secure_filename(photo.filename)
            new_photo.photo = ('static/images/' + filename)
            photo.save(os.path.join(basedir, 'static/images/' + filename))
            club_admin.photos.append(new_photo)
            db.session.commit()
            flash('Photo Added!')
            time.sleep(2.5)
            return redirect(f"/club_admin/{id}")

        if 'update_club' in request.form:
            if update_form.validate_on_submit():
                if update_form.name.data:
                    club_admin.name = update_form.name.data
                if update_form.description.data:
                    club_admin.description = update_form.description.data
                if update_form.pro_photo.data:
                    photo = update_form.pro_photo.data
                    filename = secure_filename(photo.filename)
                    club_admin.pro_photo = 'static/images/' + filename
                    photo.save(os.path.join(basedir, 'static/images/' + filename))
                if update_form.club_room.data:
                    club_admin.club_room = update_form.club_room.data
                if update_form.organiser.data:
                    club_admin.organiser = update_form.organiser.data
                db.session.commit()
                flash('Club Updated!')
                time.sleep(2.5)
                return redirect(f"/club_admin/{id}")

    # Set forms with exsisting values
    update_form.name.data = club_admin.name
    update_form.description.data = club_admin.description
    update_form.pro_photo.data = club_admin.pro_photo
    update_form.club_room.data = club_admin.club_room
    update_form.organiser.data = club_admin.organiser

    return render_template('club_admin.html', title="Club Admin Access Page",
                           notice_form=notice_form, club_admin=club_admin,
                           event_form=event_form, photo_form=photo_form,
                           update_form=update_form)


@app.context_processor
def inject_is_admin():
    if current_user.is_authenticated:
        admin_emails = [admin.email for admin in models.Admins.query.all()]
        is_admin = current_user.email in admin_emails
    else:
        is_admin = False
    return dict(is_admin=is_admin)


@app.route('/admin_access', methods=['GET', 'POST'])
@login_required
def admin():
    club_form = Add_Club()
    teacher_form = Add_Teacher()
    admin_form = Add_Admin()
    teacher_club_form = Club_Teacher()
    remove_club_form = Remove_Club()
    remove_teacher_form = Remove_Teacher()
    remove_admin_form = Remove_Admin()
    admin_emails = [admin.email for admin in models.Admins.query.all()]
    admins = models.Admins.query.all()
    teachers = models.Teachers.query.all()
    clubs = models.Clubs.query.all()
    teacher_club_form.teacher.choices = [(teacher.id, teacher.name) for teacher in teachers]
    teacher_club_form.club.choices = [(club.id, club.name) for club in clubs]
    remove_club_form.club.choices = [(club.id, club.name) for club in clubs]
    remove_teacher_form.teacher.choices = [(teacher.id, teacher.name) for teacher in teachers]
    remove_admin_form.admin.choices = [(admin.id, admin.name) for admin in admins]

    if current_user.email not in admin_emails:
        abort(404)
    else:
        if request.method == 'GET':
            return render_template("admin.html",
                                   title="Admin Access Page",
                                   club_form=club_form,
                                   teacher_form=teacher_form,
                                   teacher_club_form=teacher_club_form,
                                   remove_club_form=remove_club_form,
                                   remove_teacher_form=remove_teacher_form,
                                   remove_admin_form=remove_admin_form,
                                   admin_form=admin_form, admins=admins)
        else:
            if club_form.validate_on_submit():
                new_club = models.Clubs()
                new_club.name = club_form.name.data
                new_club.description = club_form.description.data
                photo = club_form.pro_photo.data
                filename = secure_filename(photo.filename)
                new_club.pro_photo = ('static/images/' + filename)
                photo.save(os.path.join(basedir, 'static/images/' + filename))
                new_club.club_room = club_form.club_room.data
                new_club.organiser = club_form.organiser.data
                db.session.add(new_club)
                db.session.commit()
                flash('New Club Added!')
                time.sleep(2.5)
                return redirect('/admin_access')

            if teacher_form.validate_on_submit():
                new_teacher = models.Teachers()
                new_teacher.name = teacher_form.name.data
                new_teacher.email = teacher_form.email.data
                db.session.add(new_teacher)
                db.session.commit()
                flash('New Teacher Added!')
                time.sleep(2.5)
                return redirect('/admin_access')

            if admin_form.validate_on_submit():
                new_admin = models.Admins()
                new_admin.name = admin_form.name.data
                new_admin.email = admin_form.email.data
                db.session.add(new_admin)
                db.session.commit()
                flash('New Admin Added!')
                time.sleep(2.5)
                return redirect('/admin_access')

            if teacher_club_form.validate_on_submit():
                club_id = teacher_club_form.club.data
                teacher_id = teacher_club_form.teacher.data
                club = models.Clubs.query.filter_by(id=club_id).first()
                teacher = models.Teachers.query.filter_by(id=teacher_id).first()
                club.teachers.append(teacher)
                db.session.commit()
                flash('Teacher Gained Access to Club!')
                time.sleep(2.5)
                return redirect('/admin_access')

            if remove_club_form.validate_on_submit():
                club_id = remove_club_form.club.data
                club = models.Clubs.query.filter_by(id=club_id).first()

                if club:
                    # Delete All Relationships With Club
                    db.session.execute(models.Club_Events.delete().where(models.Club_Events.c.cid == club.id))
                    db.session.execute(models.Club_Notices.delete().where(models.Club_Notices.c.cid == club.id))
                    db.session.execute(models.Club_Photos.delete().where(models.Club_Photos.c.cid == club.id))
                    db.session.execute(models.Club_Teacher.delete().where(models.Club_Teacher.c.cid == club.id))
                    db.session.execute(models.Club_User.delete().where(models.Club_User.c.cid == club.id))
                    db.session.commit()

                    db.session.delete(club)
                    db.session.commit()
                    flash('Club and all associated relationships removed!')
                    time.sleep(2.5)
                    return redirect('/admin_access')

            if remove_teacher_form.validate_on_submit():
                teacher_id = remove_teacher_form.teacher.data
                teacher = models.Teachers.query.filter_by(id=teacher_id).first()

                if teacher:
                    db.session.execute(models.Club_Teacher.delete().where(models.Club_Teacher.c.tid == teacher.id))
                    db.session.commit()

                    db.session.delete(teacher)
                    db.session.commit()
                    flash('Teacher and all associated relationships removed!')
                    time.sleep(2.5)
                    return redirect('/admin_access')

            if remove_admin_form.validate_on_submit():
                admin_id = remove_admin_form.admin.data
                admin_to_remove = models.Admins.query.get(admin_id)
                if admin_to_remove:
                    db.session.delete(admin_to_remove)
                    db.session.commit()
                    flash('Admin removed successfully!')
                    return redirect('/admin_access')

            else:
                return render_template("admin.html",
                                       title="Admin Access Page",
                                       club_form=club_form,
                                       teacher_form=teacher_form,
                                       teacher_club_form=teacher_club_form,
                                       remove_club_form=remove_club_form,
                                       remove_teacher_form=remove_teacher_form,
                                       remove_admin_form=remove_admin_form,
                                       admin_form=admin_form, admins=admins)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
