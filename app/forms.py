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
    description = TextAreaField('description', validators=[DataRequired()])
    pro_photo = StringField('pro_photo', validators=[DataRequired()])
    club_room = StringField('club_room', validators=[DataRequired()])
    organiser = StringField('organiser', validators=[DataRequired()])

#   date = IntegerField('date', validators=[Optional(), check_date])
