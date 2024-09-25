from app import app
from flask import render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if access is required

# Set up database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "info.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'
db = SQLAlchemy(app)

import app.models as models  # Import models after initializing db
from app.forms import Add_Club, Add_Teacher, Club_Teacher, Remove_Admin, Add_Notice, Add_Event, Add_Photo, Remove_Club, Remove_Teacher, Update_Club, SearchClubForm, LoginForm, SignupForm, Add_Admin


@login_manager.user_loader
def load_user(user_id):
    # Retrieve user by primary key (user_id)
    return models.User.query.filter_by(id=user_id).first()


@app.route("/")
def home():
    return render_template("home.html", title="Home Page")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if len(form.name.data) > 20:
            flash("Username must be within 20 characters", 'error')
            return redirect(url_for('signup'))

        # Check if the email already exists in the database
        user_check = models.User.query.filter_by(email=form.email.data).first()
        if not user_check:
            # Create a new user instance and save the uploaded picture
            user = models.User()
            picture = form.picture.data
            filename = secure_filename(picture.filename)
            user.picture = ('static/images/' + filename)
            picture.save(os.path.join(basedir, 'static/images/' + filename))
            user.name = form.name.data
            user.email = form.email.data
            user.password = generate_password_hash(form.password.data, salt_length=16)
            db.session.add(user)
            db.session.commit()  # Commit the new user to the database
            login_user(user, remember=True)  # Log in the new user
            return redirect(url_for('home'))
        else:
            flash("A User with the same email already exists!", 'error')
        return redirect(url_for('signup'))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Checks if user with input email exists
        user_info = models.User.query.filter_by(email=form.email.data).first()
        # If exists, check db hash with input password and if there's a match,
        # login user
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
    flash("Logged Out!")
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
            return redirect(url_for('clubs'))
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

    return render_template("clubs.html", title="Clubs Page", clubs=clubs,
                           form=form, club_status=club_status)


@app.route("/club/<int:id>")
def club(id):
    # Check if the club with the given ID exists
    club = models.Clubs.query.filter_by(id=id).first_or_404()
    # if not club:
    #     abort(404)  # Not found if the club doesn't exist

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
@login_required
def club_admin(id):
    # Check if the club with the given ID exists
    club_admin = models.Clubs.query.filter_by(id=id).first()
    if not club_admin:
        abort(404)  # Not found if the club doesn't exist

    user_email = current_user.email

    # Check if the user is a teacher
    teacher = models.Teachers.query.filter_by(email=user_email).first()
    if not teacher:
        abort(403)  # Forbidden if the user is not a teacher

    # Check if the teacher has access to this specific club
    has_access = db.session.query(models.Club_Teacher).filter_by(cid=id, tid=teacher.id).first()
    if not has_access:
        abort(403)  # Forbidden if the teacher does not have access to the club

    # Initialize forms
    notice_form = Add_Notice()
    event_form = Add_Event()
    photo_form = Add_Photo()
    update_form = Update_Club()

    if request.method == 'POST':
        # Handle form submissions
        if 'delete_notice' in request.form:
            notice_id = request.form.get('delete_notice')
            notice_to_delete = models.Notices.query.filter_by(id=notice_id).first()
            if notice_to_delete:
                # Delete the associated photo from the file system if it exists
                if notice_to_delete.photo:
                    try:
                        os.remove(
                            os.path.join(basedir, notice_to_delete.photo))
                    except FileNotFoundError:
                        flash(f"Notice photo {notice_to_delete.photo} not found on the server.", "warning")

                club_admin.notices.remove(notice_to_delete)
                db.session.commit()
                flash('Notice Deleted!')
            return redirect(f"/club_admin/{id}")

        if 'delete_event' in request.form:
            event_id = request.form.get('delete_event')
            event_to_delete = models.Events.query.filter_by(
                id=event_id).first()
            if event_to_delete:
                # Delete the associated photo from the file system if it exists
                if event_to_delete.photo:
                    try:
                        os.remove(os.path.join(basedir, event_to_delete.photo))
                    except FileNotFoundError:
                        flash(f"Event photo {event_to_delete.photo} not found on the server.", "warning")

                club_admin.events.remove(event_to_delete)
                db.session.commit()
                flash('Event Deleted!')
            return redirect(f"/club_admin/{id}")

        if 'delete_photo' in request.form:
            photo_id = request.form.get('delete_photo')
            photo_to_delete = models.Photos.query.filter_by(id=photo_id).first()
            if photo_to_delete:
                # Delete the associated photo from the file system if it exists
                if photo_to_delete.photo:
                    try:
                        os.remove(os.path.join(basedir, photo_to_delete.photo))
                    except FileNotFoundError:
                        flash(f"Notice photo {photo_to_delete.photo} not found on the server.", "warning")

                club_admin.photos.remove(photo_to_delete)
                db.session.commit()
                flash('Photo Deleted!')
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
            return redirect(f"/club_admin/{id}")

        if event_form.validate_on_submit():
            new_event = models.Events()
            new_event.name = event_form.name.data
            new_event.date = event_form.date.data
            new_event.location = event_form.location.data
            photo = event_form.photo.data
            filename = secure_filename(photo.filename)
            new_event.photo = ('static/images/' + filename)
            photo.save(os.path.join(basedir, 'static/images/' + filename))
            club_admin.events.append(new_event)
            db.session.commit()
            flash('Event Added!')
            return redirect(f"/club_admin/{id}")

        if photo_form.validate_on_submit():
            new_photo = models.Photos()
            new_photo.description = photo_form.description.data
            photo = photo_form.photo.data
            filename = secure_filename(photo.filename)
            new_photo.photo = ('static/images/' + filename)
            photo.save(os.path.join(basedir, 'static/images/' + filename))
            club_admin.photos.append(new_photo)
            db.session.commit()
            flash('Photo Added!')
            return redirect(f"/club_admin/{id}")

        if 'update_club' in request.form:
            # Update information about the club if provided
            if update_form.validate_on_submit():
                if update_form.name.data:
                    club_admin.name = update_form.name.data
                if update_form.description.data:
                    club_admin.description = update_form.description.data
                if update_form.pro_photo.data:
                    photo = update_form.pro_photo.data
                    filename = secure_filename(photo.filename)
                    club_admin.pro_photo = 'static/images/' + filename
                    photo.save(os.path.join(
                        basedir, 'static/images/' + filename))
                if update_form.club_room.data:
                    club_admin.club_room = update_form.club_room.data
                if update_form.organiser.data:
                    club_admin.organiser = update_form.organiser.data

                # Commit changes and flash success message
                db.session.commit()
                flash('Club Updated!')
                return redirect(f"/club_admin/{id}")

    return render_template('club_admin.html',
                           title="Club Admin Access Page",
                           notice_form=notice_form, club_admin=club_admin,
                           event_form=event_form, photo_form=photo_form,
                           update_form=update_form)


@app.context_processor
def inject_is_admin():
    if current_user.is_authenticated:
        # Get all admin emails to check if current user is an admin
        admin_emails = [admin.email for admin in models.Admins.query.all()]
        is_admin = current_user.email in admin_emails
    else:
        is_admin = False
    return dict(is_admin=is_admin)


@app.route('/admin_access', methods=['GET', 'POST'])
@login_required
def admin():
    # Initialize forms for admin actions
    club_form = Add_Club()
    teacher_form = Add_Teacher()
    admin_form = Add_Admin()
    teacher_club_form = Club_Teacher()
    remove_club_form = Remove_Club()
    remove_teacher_form = Remove_Teacher()
    remove_admin_form = Remove_Admin()

    # Retrieve all necessary data from the database
    admins = models.Admins.query.all()
    teachers = models.Teachers.query.all()
    clubs = models.Clubs.query.all()
    users = models.User.query.all()  # Fetch all users

    # Prepare email lists for admins and teachers
    admin_emails = [admin.email for admin in models.Admins.query.all()]
    teacher_emails = [teacher.email for teacher in teachers]
    re_admin_emails = [admin.email for admin in admins]

    # Get user data for admin and teacher forms
    teacher_users = models.User.query.filter(models.User.email.in_(teacher_emails)).all()
    admin_users = models.User.query.filter(models.User.email.in_(re_admin_emails)).all()

    # Populate select fields for forms with user options
    teacher_club_form.teacher.choices = [(teacher.id, teacher.email) for teacher in teachers]
    teacher_club_form.club.choices = [(club.id, club.name) for club in clubs]
    remove_club_form.club.choices = [(club.id, club.name) for club in clubs]
    remove_teacher_form.teacher.choices = [(teacher.id, teacher.email) for teacher in teachers]
    remove_admin_form.admin.choices = [(admin.id, admin.email) for admin in admins]

    # Populate forms with user data, including names and emails
    teacher_club_form.teacher.choices = [(user.id, f"{user.name} - {user.email}") for user in teacher_users]
    teacher_form.email.choices = [(user.id, f"{user.name} - {user.email}") for user in users]
    admin_form.email.choices = [(user.id, f"{user.name} - {user.email}") for user in users]
    remove_teacher_form.teacher.choices = [(user.id, f"{user.name} - {user.email}") for user in teacher_users]
    remove_admin_form.admin.choices = [(user.id, f"{user.name} - {user.email}") for user in admin_users]

    if current_user.email not in admin_emails:
        abort(403)
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
                flash(f'{new_club.name} Club Added!')
                return redirect('/admin_access')

            if teacher_form.validate_on_submit():
                # Get the user ID from the form and look up the email
                user_id = teacher_form.email.data
                user = models.User.query.get(user_id)
                new_teacher = models.Teachers()
                new_teacher.email = user.email  # Save the email
                db.session.add(new_teacher)
                db.session.commit()
                flash('Teacher Access Given!')
                return redirect('/admin_access')

            if admin_form.validate_on_submit():
                # Get the user ID from the form and look up the email
                user_id = admin_form.email.data
                user = models.User.query.get(user_id)
                new_admin = models.Admins()
                new_admin.email = user.email  # Save the email
                db.session.add(new_admin)
                db.session.commit()
                flash('Admin Access Given!')
                return redirect('/admin_access')

            if teacher_club_form.validate_on_submit():
                club_id = teacher_club_form.club.data
                user_id = teacher_club_form.teacher.data
                user = models.User.query.get(user_id)
                teacher = models.Teachers.query.filter_by(
                    email=user.email).first()
                if not teacher:
                    teacher = models.Teachers(email=user.email)
                    db.session.add(teacher)
                    db.session.commit()
                club = models.Clubs.query.get(club_id)
                club.teachers.append(teacher)
                db.session.commit()
                flash('Teacher Gained Access To Club!')
                return redirect('/admin_access')

            if remove_club_form.validate_on_submit():
                club_id = remove_club_form.club.data
                club = models.Clubs.query.filter_by(id=club_id).first()

                if club:
                    # Remove the profile photo from the file system
                    if club.pro_photo:
                        try:
                            os.remove(os.path.join(basedir, club.pro_photo))
                        except FileNotFoundError:
                            flash(f"Profile photo {club.pro_photo} not found on the server.", "warning")

                    # Delete All Relationships With Club
                    db.session.execute(models.Club_Events.delete().where(models.Club_Events.c.cid == club.id))
                    db.session.execute(models.Club_Notices.delete().where(models.Club_Notices.c.cid == club.id))
                    db.session.execute(models.Club_Photos.delete().where(models.Club_Photos.c.cid == club.id))
                    db.session.execute(models.Club_Teacher.delete().where(models.Club_Teacher.c.cid == club.id))
                    db.session.execute(models.Club_User.delete().where(models.Club_User.c.cid == club.id))
                    db.session.commit()

                    db.session.delete(club)
                    db.session.commit()
                    flash('Club Deleted!')
                    return redirect('/admin_access')

            if remove_teacher_form.validate_on_submit():
                user_id = remove_teacher_form.teacher.data
                user = models.User.query.get(user_id)
                teacher = models.Teachers.query.filter_by(email=user.email).first()

                if teacher:
                    db.session.execute(models.Club_Teacher.delete().where(models.Club_Teacher.c.tid == teacher.id))
                    db.session.commit()

                    db.session.delete(teacher)
                    db.session.commit()
                    flash('Teacher Removed')
                    return redirect('/admin_access')

            if remove_admin_form.validate_on_submit():
                user_id = remove_admin_form.admin.data
                user = models.User.query.get(user_id)
                admin_to_remove = models.Admins.query.filter_by(email=user.email).first()

                if admin_to_remove:
                    db.session.delete(admin_to_remove)
                    db.session.commit()
                    flash('Admin Removed')
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


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


if __name__ == "__main__":
    app.run(debug=True)
