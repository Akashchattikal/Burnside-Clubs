from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, FileField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from wtforms import validators
import app.models
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileAllowed


# Admin Page

class Add_Club(FlaskForm):

    name = StringField('title', validators=[DataRequired(), Length(max=30)],
                       render_kw={"class": "form_name rounded-input",
                                  "placeholder": "Avoid Adding 'Club' At End"})
    description = TextAreaField('description',
                                validators=[DataRequired(), Length(max=500)],
                                render_kw={"class": "form_desc rounded-input"})
    pro_photo = FileField('pro_photo',
                          validators=[DataRequired(),
                                      FileAllowed(['jpg', 'jpeg', 'png',
                                                   'gif'], 'Images only!')],
                          render_kw={"class": "form_pic custom-file-upload",
                                     "id": "inputFile",
                                     "accept": ".jpg,.jpeg,.png,.gif"})
    club_room = StringField('club_room',
                            validators=[DataRequired(), Length(max=10)],
                            render_kw={"class": "form_room rounded-input"})
    organiser = StringField('organiser',
                            validators=[DataRequired(), Length(max=20)],
                            render_kw={"class": "form_organiser\
                                       rounded-input"})
    submit = SubmitField('Add', render_kw={"class": "submission rounded-20"})


class Add_Teacher(FlaskForm):

    email = SelectField('email', validators=[DataRequired()],
                        render_kw={"class": "form_email rounded-input"})
    submit = SubmitField('Add', render_kw={"class": "submission rounded-20"})


class Add_Admin(FlaskForm):
    email_admin = SelectField('email', validators=[DataRequired()],
                              render_kw={"class": "form_email rounded-input"})
    submit = SubmitField('Add', render_kw={"class": "submission rounded-20"})


class Club_Teacher(FlaskForm):

    club = SelectField('club', validators=[DataRequired()],
                       render_kw={"class": "small_form"})
    teacher = SelectField('teacher', validators=[DataRequired()],
                          render_kw={"class": "common_form"})
    submit = SubmitField('Assign',
                         render_kw={"class": "submission rounded-20"})


class Remove_Club(FlaskForm):

    club = SelectField('Club', coerce=int, validators=[DataRequired()],
                       render_kw={"class": "small_form"})
    submit = SubmitField('Delete',
                         render_kw={"class": "submission rounded-20"})


class Remove_Teacher(FlaskForm):

    teacher = SelectField('Select Teacher',
                          coerce=int, render_kw={"class": "common_form"})
    submit = SubmitField('Remove',
                         render_kw={"class": "submission rounded-20"})


class Remove_Admin(FlaskForm):

    admin = SelectField('Select Admin',
                        coerce=int, render_kw={"class": "common_form"})
    submit = SubmitField('Remove',
                         render_kw={"class": "submission rounded-20"})


#  Club Admin


class Add_Notice(FlaskForm):

    notice = StringField('notice', validators=[DataRequired(),
                                               Length(max=125)],
                         render_kw={"class": "form_add add_in_order",
                                    "placeholder": "Enter Notice Details"})
    photo = FileField('photo',
                      validators=[DataRequired(),
                                  FileAllowed(['jpg', 'jpeg',
                                               'png', 'gif'], 'Images only!')],
                      render_kw={"class": "form_add add_in_order\
                                 add_notice_prop",
                                 "id": "inputFile",
                                 "accept": ".jpg,.jpeg,.png,.gif"})
    date = DateField('date', format='%Y-%m-%d',
                     render_kw={"class": "form_add add_in_order"})


class Add_Event(FlaskForm):

    name = StringField('name',
                       validators=[DataRequired(), Length(max=125)],
                       render_kw={"class": "form_add add_in_order",
                                  "placeholder": "Enter Event Details"})
    location = StringField('location',
                           validators=[DataRequired(), Length(max=100)],
                           render_kw={"class": "form_add add_in_order",
                                      "placeholder": "Enter Event Location"})
    photo = FileField('photo',
                      validators=[DataRequired(),
                                  FileAllowed(['jpg', 'jpeg',
                                               'png', 'gif'], 'Images only!')],
                      render_kw={"class": "form_add add_in_order\
                                 add_event_prop",
                                 "id": "inputFile",
                                 "accept": ".jpg,.jpeg,.png,.gif"})
    date = DateField('date', validators=[DataRequired()],
                     format='%Y-%m-%d',
                     render_kw={"class": "form_add add_in_order"})


class Add_Photo(FlaskForm):

    photo = FileField('photo',
                      validators=[DataRequired(),
                                  FileAllowed(['jpg', 'jpeg',
                                               'png', 'gif'], 'Images only!')],
                      render_kw={"class": "form_add_photo add_in_order",
                                 "id": "inputFile",
                                 "accept": ".jpg,.jpeg,.png,.gif"})
    description = StringField('description',
                              validators=[DataRequired(), Length(max=100)],
                              render_kw={"class": "form_add_photo\
                                         add_in_order",
                                         "placeholder": "Enter Photo Details"})


class Update_Club(FlaskForm):

    name = StringField('Name', validators=[Length(max=30)],
                       render_kw={"class": "form_change_center rounded-input",
                                  "placeholder": "Enter New Club Name"})
    description = StringField('Description', validators=[Length(max=500)],
                              render_kw={"class": "form_change_desc\
                                          rounded-input",
                                         "placeholder": "Enter\
                                         New Description"})
    pro_photo = FileField('Profile Photo',
                          validators=[
                              FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                          'Images only!')],
                          render_kw={"class": "form_change_file\
                                     custom-file-upload",
                                     "id": "inputFile",
                                     "accept": ".jpg,.jpeg,.png,.gif"})
    club_room = StringField('Club Common Room', validators=[Length(max=10)],
                            render_kw={"class": "form_change_center\
                                       rounded-input",
                                       "placeholder": "Enter New Club Room"})
    organiser = StringField('Organiser',
                            validators=[Length(max=20)],
                            render_kw={"class": "form_change_organiser\
                                       rounded-input",
                                       "placeholder": "Enter New Organiser"})
    submit = SubmitField('Update Club')


#  Clubs

class SearchClubForm(FlaskForm):
    search_query = StringField('Search',
                               validators=[DataRequired()],
                               render_kw={"class": "club_search",
                                          "placeholder": "🔍\
                                          Search For A Club"})
    submit = SubmitField('Search', render_kw={"class": "search_button"})


#  Login

class LoginForm(FlaskForm):
    email = EmailField("Email",
                       validators=[DataRequired(), Email(), Length(max=254)],
                       render_kw={"class": "login",
                                  "placeholder": "Enter Email"})
    password = PasswordField("Password",
                             validators=[DataRequired()],
                             render_kw={"class": "login",
                                        "placeholder": "Enter Password"})
    submit = SubmitField("Submit", render_kw={"class": "log_sub"})


# Sign Up

class SignupForm(FlaskForm):
    picture = FileField('Profile Photo',
                        validators=[DataRequired(),
                                    FileAllowed(['jpg', 'jpeg',
                                                 'png', 'gif'], '\
                                                    Images only!')],
                        render_kw={"class": "signup_file", "id": "inputFile",
                                   "accept": ".jpg,.jpeg,.png,.gif"})
    name = StringField("Name",
                       validators=[DataRequired(),
                                   Length(max=20, message="Username must\
                                          be within 20 characters")],
                       render_kw={"class": "signup",
                                  "placeholder": "Enter A Username"})
    email = EmailField("Email",
                       validators=[DataRequired(), Email(), Length(max=254)],
                       render_kw={"class": "signup",
                                  "placeholder": "Enter An Email"})
    password = PasswordField("Password",
                             validators=[DataRequired()],
                             render_kw={"class": "signup",
                                        "placeholder": "Enter A Password"})
    repassword = PasswordField("Re Enter Password",
                               validators=[DataRequired()],
                               render_kw={"class": "signup",
                                          "placeholder": "Re Enter Password"})
    submit = SubmitField("Submit", render_kw={"class": "sign_sub"})
