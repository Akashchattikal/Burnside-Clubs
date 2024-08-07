from app import app
from flask import render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import time
from werkzeug.utils import secure_filename


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "info.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)

import app.models as models  # need 'db' to import models
from app.forms import Add_Club, Add_Teacher, Club_Teacher,  Add_Notice, Add_Event, Add_Photo, Remove_Club, Remove_Teacher


@app.route("/")
def home():
    return render_template("home.html", title="Home Page")


@app.route("/clubs")
def clubs():
    clubs = models.Clubs.query.all()
    return render_template("clubs.html", title="Clubs Page", clubs=clubs)


@app.route("/club/<int:id>")
def club(id):
    club = models.Clubs.query.filter_by(id=id).first()

    return render_template('club.html', club=club)


@app.route("/teach_access")
def teachers():
    teachers = models.Teachers.query.all()
    return render_template("teachers.html", title="Teach Access Page", teachers=teachers)


@app.route("/teach/<int:id>")
def teacher(id):
    teacher = models.Teachers.query.filter_by(id=id).first()
    return render_template("teacher.html", title="Club Access Page", teacher=teacher)


@app.route("/club_admin/<int:id>", methods=['GET', 'POST'])
def club_admin(id):

    club_admin = models.Clubs.query.filter_by(id=id).first()
    notice_form = Add_Notice()
    event_form = Add_Event()
    photo_form = Add_Photo()
    if request.method == 'GET':
        return render_template('club_admin.html', title="Club Admin Access Page", notice_form=notice_form, club_admin=club_admin, event_form=event_form, photo_form=photo_form)
    else:
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
        else:
            return render_template('club_admin.html', title="Club Admin Access Page", notice_form=notice_form, club_admin=club_admin, event_form=event_form, photo_form=photo_form)


@app.route('/admin_access', methods=['GET', 'POST'])
def admin():
    club_form = Add_Club()
    teacher_form = Add_Teacher()
    teacher_club_form = Club_Teacher()
    remove_club_form = Remove_Club()
    remove_teacher_form = Remove_Teacher()

    teachers = models.Teachers.query.all()
    clubs = models.Clubs.query.all()
    teacher_club_form.teacher.choices = [(teacher.id, teacher.name) for teacher in teachers]
    teacher_club_form.club.choices = [(club.id, club.name) for club in clubs]
    remove_club_form.club.choices = [(club.id, club.name) for club in clubs]
    remove_teacher_form.teacher.choices = [(teacher.id, teacher.name) for teacher in teachers]

    if request.method == 'GET':
        return render_template("admin.html", title="Admin Access Page", club_form=club_form, teacher_form=teacher_form, teacher_club_form=teacher_club_form, remove_club_form=remove_club_form, remove_teacher_form=remove_teacher_form)
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

        else:
            return render_template("admin.html", title="Admin Access Page", club_form=club_form, teacher_form=teacher_form, teacher_club_form=teacher_club_form, remove_club_form=remove_club_form, remove_teacher_form=remove_teacher_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
