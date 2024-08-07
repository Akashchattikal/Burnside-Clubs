from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, EmailField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from wtforms import validators
import app.models
from datetime import datetime


class Add_Club(FlaskForm):

    name = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    pro_photo = FileField('pro_photo', validators=[DataRequired()])
    club_room = StringField('club_room', validators=[DataRequired()])
    organiser = StringField('organiser', validators=[DataRequired()])


class Add_Teacher(FlaskForm):

    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired()])

#  validators.Email()


class Add_Notice(FlaskForm):

    # def check_date(form, field):
    #     _current_date = int(datetime.now().year)
    #     if field.data < _current_date:
    #         raise ValidationError("You can't enter a date from the past!")

    notice = StringField('notice')  # , validators=[DataRequired()])
    photo = FileField('photo', validators=[DataRequired()])
    date = DateField('date', format='%Y-%m-%d')

# IntegerField('date', validators=[Optional(), check_date])


class Add_Event(FlaskForm):

    name = StringField('name', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    photo = FileField('photo', validators=[DataRequired()])
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d')


class Club_Teacher(FlaskForm):
    club = SelectField('club', validators=[DataRequired()])
    teacher = SelectField('teacher', validators=[DataRequired()])


class Add_Photo(FlaskForm):

    photo = FileField('photo', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class Find_Club(FlaskForm):

    club_name = SelectField('club_name', validators=[DataRequired()], coerce=int)


class Remove_Club(FlaskForm):
    club = SelectField('Club', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Remove Club')


class Remove_Teacher(FlaskForm):
    teacher = SelectField('Select Teacher', coerce=int)
    submit = SubmitField('Remove Teacher')
