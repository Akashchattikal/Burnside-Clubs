from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, EmailField, FileField
from wtforms.validators import DataRequired, Optional, ValidationError
from wtforms import validators
import app.models
from datetime import datetime


class Add_Club(FlaskForm):

    name = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    pro_photo = StringField('pro_photo', validators=[DataRequired()])
    club_room = StringField('club_room', validators=[DataRequired()])
    organiser = StringField('organiser', validators=[DataRequired()])


class Add_Teacher(FlaskForm):

    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired()])

#  validators.Email()

class Add_Notice(FlaskForm):

    def check_date(form, field):
        _current_date = int(datetime.now().year)
        if field.data < _current_date:
            raise ValidationError("You can't enter a date from the past!")

    notice = StringField('name', validators=[DataRequired()])
    date = IntegerField('date', validators=[Optional(), check_date])


class Club_Teacher(FlaskForm):

    club = SelectField('club', validators=[DataRequired()])
    teacher = SelectField('teacher', validators=[DataRequired()])
