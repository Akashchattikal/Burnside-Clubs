from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, EmailField, FileField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError, InputRequired, Length, EqualTo, Email
from wtforms import validators
import app.models
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField


# Admin Page

class Add_Club(FlaskForm):

    name = StringField('title', validators=[DataRequired()], render_kw={"class": "form_name rounded-input", "placeholder": "Avoid Adding 'Club' At End"})
    description = TextAreaField('description', validators=[DataRequired()], render_kw={"class": "form_desc rounded-input"})
    pro_photo = FileField('pro_photo', validators=[DataRequired()], render_kw={"class": "form_pic custom-file-upload"})
    club_room = StringField('club_room', validators=[DataRequired()], render_kw={"class": "form_room rounded-input"})
    organiser = StringField('organiser', validators=[DataRequired()], render_kw={"class": "form_organiser rounded-input"})


class Add_Teacher(FlaskForm):

    email = SelectField('email', validators=[DataRequired()], render_kw={"class": "form_email rounded-input"})


class Add_Admin(FlaskForm):
    email = SelectField('email', validators=[DataRequired()], render_kw={"class": "form_email rounded-input"})
    submit = SubmitField('Add', render_kw={"class": "submission rounded-20"})


class Club_Teacher(FlaskForm):

    club = SelectField('club', validators=[DataRequired()], render_kw={"class": "small_form"})
    teacher = SelectField('teacher', validators=[DataRequired()], render_kw={"class": "common_form"})


class Remove_Club(FlaskForm):

    club = SelectField('Club', coerce=int, validators=[DataRequired()], render_kw={"class": "small_form"})
    submit = SubmitField('Delete')


class Remove_Teacher(FlaskForm):

    teacher = SelectField('Select Teacher', coerce=int, render_kw={"class": "common_form"})
    submit = SubmitField('Remove')


class Remove_Admin(FlaskForm):

    admin = SelectField('Select Admin', coerce=int, render_kw={"class": "common_form"})
    submit = SubmitField('Remove')


#  Club Admin


class Add_Notice(FlaskForm):

    notice = StringField('notice', validators=[DataRequired()], render_kw={"class": "form_add add_in_order", "placeholder": "Enter Notice Details"})
    photo = FileField('photo', validators=[DataRequired()], render_kw={"class": "form_add add_in_order add_notice_prop"})
    date = DateField('date', format='%Y-%m-%d', render_kw={"class": "form_add add_in_order"})


class Add_Event(FlaskForm):

    name = StringField('name', validators=[DataRequired()], render_kw={"class": "form_add add_in_order", "placeholder": "Enter Event Details"})
    location = StringField('location', validators=[DataRequired()], render_kw={"class": "form_add add_in_order", "placeholder": "Enter Event Location"})
    photo = FileField('photo', validators=[DataRequired()], render_kw={"class": "form_add add_in_order add_event_prop"})
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"class": "form_add add_in_order"})


class Add_Photo(FlaskForm):

    photo = FileField('photo', validators=[DataRequired()], render_kw={"class": "form_add_photo add_in_order"})
    description = StringField('description', validators=[DataRequired()], render_kw={"class": "form_add_photo add_in_order", "placeholder": "Enter Photo Details"})


class Update_Club(FlaskForm):

    name = StringField('Name', render_kw={"class": "form_change_center rounded-input", "placeholder": "Enter New Club Name"})
    description = StringField('Description', render_kw={"class": "form_change_desc rounded-input", "placeholder": "Enter New Description"})
    pro_photo = FileField('Profile Photo', render_kw={"class": "form_change_file custom-file-upload"})
    club_room = StringField('Club Common Room', render_kw={"class": "form_change_center rounded-input", "placeholder": "Enter New Club Room"})
    organiser = StringField('Organiser', render_kw={"class": "form_change_organiser rounded-input", "placeholder": "Enter New Organiser"})
    submit = SubmitField('Update Club')


#  Clubs

class SearchClubForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()], render_kw={"class": "club_search", "placeholder": "🔍 Search For A Club"})
    submit = SubmitField('Search', render_kw={"class": "search_button"})


#  Login

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()], render_kw={"class": "login", "placeholder": "Enter Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"class": "login", "placeholder": "Enter Password"})
    submit = SubmitField("Submit", render_kw={"class": "log_sub"})


# Sign Up

class SignupForm(FlaskForm):
    picture = FileField('Profile Photo', validators=[DataRequired()], render_kw={"class": "signup_file"})
    name = StringField("Name", validators=[DataRequired()], render_kw={"class": "signup", "placeholder": "Enter A Name"})
    email = EmailField("Email", validators=[DataRequired(), Email()], render_kw={"class": "signup", "placeholder": "Enter A Email"})
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('repassword', message="the passful words must match-a-block")], render_kw={"class": "signup", "placeholder": "Enter A Password"})
    repassword = PasswordField("Re Enter Password", validators=[DataRequired()], render_kw={"class": "signup", "placeholder": "Re Enter Password"})
    submit = SubmitField("Submit", render_kw={"class": "sign_sub"})
