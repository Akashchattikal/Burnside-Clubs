from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models
from datetime import datetime


class Add_Club(FlaskForm):

    # def check_date(form, field):
    #   _current_date = int(datetime.now().year)
    #   if field.data > _current_date:
    #     raise ValidationError("You can't enter a date from the future!")

    name = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description')
    pro_photo = TextAreaField('pro_photo')
    club_room = TextAreaField('club_room')
    organiser = TextAreaField('organiser')

#   date = IntegerField('date', validators=[Optional(), check_date])
