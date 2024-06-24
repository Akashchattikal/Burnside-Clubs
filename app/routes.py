from app import app
from flask import render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "info.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)

import app.models as models  # need 'db' to import models
from app.forms import Add_Club, Add_Teacher, Club_Teacher

    
@app.route("/")
def home():
    return render_template("home.html", title="Home Page")


@app.route("/clubs")
def clubs():
    clubs = models.Clubs.query.all()
    return render_template("clubs.html", title="Clubs Page", clubs=clubs)


@app.route("/club/<int:id>")
def Club(id):
    club = models.Clubs.query.filter_by(id=id).first()
    return render_template('club.html', club=club)


@app.route("/teach_access")
def teach():
    return render_template("teach.html", title="Teach Access Page")


@app.route('/admin_access', methods=['GET', 'POST'])
def admin():
    club_form = Add_Club()
    teacher_form = Add_Teacher()
    teacher_club_form = Club_Teacher()
    teachers = models.Teachers.query.all()
    clubs = models.Clubs.query.all()
    teacher_club_form.teacher.choices = [(teacher.id, teacher.name) for teacher in teachers]
    teacher_club_form.club.choices = [(club.id, club.name) for club in clubs]
    if request.method == 'GET':
        return render_template("admin.html", title="Admin Access Page", club_form=club_form, teacher_form=teacher_form, teacher_club_form=teacher_club_form)
    else:
        if club_form.validate_on_submit():
            new_club = models.Clubs()
            new_club.name = club_form.name.data
            new_club.description = club_form.description.data
            new_club.pro_photo = club_form.pro_photo.data
            new_club.club_room = club_form.club_room.data
            new_club.organiser = club_form.organiser.data
            db.session.add(new_club)
            db.session.commit()
            return redirect('/admin_access')

        if teacher_form.validate_on_submit():
            new_teacher = models.Teachers()
            new_teacher.name = teacher_form.name.data
            new_teacher.email = teacher_form.email.data
            db.session.add(new_teacher)
            db.session.commit()
            return redirect('/admin_access')

        if teacher_club_form.validate_on_submit():
            club_teacher = models.Club_Teacher()
            club_teacher.club = teacher_club_form.club.data
            club_teacher.teacher = teacher_club_form.teacher.data
            db.session.add(club_teacher)
            db.session.commit()
            return redirect('/admin_access')

        else:
            # note the terrible logic, this has already been called once in
            # this function - could the logic be tidied up?
            return render_template("admin.html", title="Admin Access Page", club_form=club_form, teacher_form=teacher_form, teacher_club_form=teacher_club_form)


if __name__ == "__main__":
    app.run(debug=True)
