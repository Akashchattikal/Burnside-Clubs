from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, EmailField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from wtforms import validators
import app.models
from datetime import datetime


class Add_Club(FlaskForm):

    name = StringField('title', validators=[DataRequired()], render_kw={"class": "form_name rounded-input"})
    description = TextAreaField('description', validators=[DataRequired()], render_kw={"class": "form_desc rounded-input"})
    pro_photo = FileField('pro_photo', validators=[DataRequired()], render_kw={"class": "form_pic file-input custom-file-upload"})
    club_room = StringField('club_room', validators=[DataRequired()], render_kw={"class": "form_room rounded-input"})
    organiser = StringField('organiser', validators=[DataRequired()], render_kw={"class": "form_organiser rounded-input"})


class Add_Teacher(FlaskForm):

    name = StringField('name', validators=[DataRequired()], render_kw={"class": "form_name rounded-input"})
    email = EmailField('email', validators=[validators.DataRequired()], render_kw={"class": "form_email rounded-input"})

#  validators.Email()


class Add_Notice(FlaskForm):

    # def check_date(form, field):
    #     _current_date = int(datetime.now().year)
    #     if field.data < _current_date:
    #         raise ValidationError("You can't enter a date from the past!")

    notice = StringField('notice', validators=[DataRequired()], render_kw={"class": "form_add"})
    photo = FileField('photo', validators=[DataRequired()], render_kw={"class": "form_add"})
    date = DateField('date', format='%Y-%m-%d', render_kw={"class": "form_add"})

# IntegerField('date', validators=[Optional(), check_date])


class Add_Event(FlaskForm):

    name = StringField('name', validators=[DataRequired()], render_kw={"class": "form_add"})
    location = StringField('location', validators=[DataRequired()], render_kw={"class": "form_add"})
    photo = FileField('photo', validators=[DataRequired()], render_kw={"class": "form_add"})
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"class": "form_add"})


class Club_Teacher(FlaskForm):
    club = SelectField('club', validators=[DataRequired()], render_kw={"class": "custom-select"})
    teacher = SelectField('teacher', validators=[DataRequired()], render_kw={"class": "custom-select"})


class Add_Photo(FlaskForm):

    photo = FileField('photo', validators=[DataRequired()], render_kw={"class": "form_add_photo"})
    description = StringField('description', validators=[DataRequired()], render_kw={"class": "form_add_photo"})


class Find_Club(FlaskForm):

    club_name = SelectField('club_name', validators=[DataRequired()], coerce=int)


class Remove_Club(FlaskForm):
    club = SelectField('Club', coerce=int, validators=[DataRequired()], render_kw={"class": "custom-select"})
    submit = SubmitField('Remove Club')


class Remove_Teacher(FlaskForm):
    teacher = SelectField('Select Teacher', coerce=int, render_kw={"class": "custom-select"})
    submit = SubmitField('Remove Teacher')


class Update_Club(FlaskForm):
    name = StringField('Name', render_kw={"class": "form_change_center rounded-input", "placeholder": "Enter New Club Name"})
    description = StringField('Description', render_kw={"class": "form_change_desc rounded-input", "placeholder": "Enter New Description"})
    pro_photo = FileField('Profile Photo', render_kw={"class": "form_change_file custom-file-upload"})
    club_room = StringField('Club Common Room', render_kw={"class": "form_change_center rounded-input", "placeholder": "Enter New Club Room"})
    organiser = StringField('Organiser', render_kw={"class": "form_change_organiser rounded-input", "placeholder": "Enter New Organiser"})
    submit = SubmitField('Update Club')
