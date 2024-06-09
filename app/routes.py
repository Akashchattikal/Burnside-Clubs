from app import app
from flask import render_template, abort, request, redirect
# from flask_sqlalchemy import SQLAlchemy # no more boring old SQL for us!
# import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# db = SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "clubs.db")
# db.init_app(app)

# import app.models as models


@app.route("/")
def home():
    return render_template("home.html", title="Home Page")
