from app import app
from flask import render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import app.models as models # need 'db' to import models
from app.forms import Add_Club


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "info.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template("home.html", title="Home Page")


@app.route("/clubs")
def clubs():
    clubs = models.Clubs.query.all()
    return render_template("clubs.html", title="Clubs Page", clubs=clubs)


@app.route("/admin_access")
def admin():
    return render_template("admin.html", title="Admin Access Page")


@app.route('/teach_access', methods=['GET', 'POST'])
def teach():
    form = Add_Club()
    if request.method == 'GET':
        return render_template("teach.html",
                               title="Teacher Access Page", form=form)
    else:
        if form.validate_on_submit():
            new_club = models.Clubs()
            new_club.name = form.name.data
            new_club.description = form.description.data
            new_club.pro_photo = form.pro_photo.data
            new_club.club_room = form.club_room.data
            new_club.organiser = form.organiser.data
            db.session.add(new_club)
            db.session.commit()
            return redirect('/clubs')
        else:
            # note the terrible logic, this has already been called once in
            # this function - could the logic be tidied up?
            return render_template("teach.html",
                                   title="Teacher Access Page", form=form)


if __name__ == "__main__":
    app.run(debug=True)