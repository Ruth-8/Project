from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
import app
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField("Confirm Password", [EqualTo('password', "Passwords needs to match.")])
    submit = SubmitField('Register')

    def verify_name(self, name):
        user = app.User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This name is not valid.Please enter another name.')

    def verify_email(self, email):
        user = app.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is not valid.Please enter another name.')


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Keep me logged in")
    submit = SubmitField('Prisijungti')

class UserUpdateForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def verify_name(self, name):
        if name.data != app.current_user.name:
            user = app.User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('This name is not valid.Please enter another name.')

    def verify_email(self, email):
        if email.data != app.current_user.email:
            user = app.User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is not valid.Please enter another name.')

class PatientForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    surname = StringField('Surname', [DataRequired()])
    email =StringField('Email', [DataRequired()])
    phone = StringField ('Phone number', [DataRequired()])
    relationship =StringField('Next of Kin', [DataRequired()])
    treatment =StringField('Treatment plan', [DataRequired()], widget=TextArea())
    submit = SubmitField ("Submit")

class NotesForm(FlaskForm):
    sender = StringField('From', [DataRequired()])
    receiver = StringField('To', [DataRequired()])
    notes =StringField('Notes', [DataRequired()], widget=TextArea())
    submit = SubmitField ("Submit")







