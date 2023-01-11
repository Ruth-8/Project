from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from Project.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField("Confirm Password", [EqualTo('password', "Passwords needs to match.")])
    submit = SubmitField('Register')

    def verify_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This name is not valid.Please enter another name.')

    def verify_email(self, email):
        user = User.query.filter_by(email=email.data).first()
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
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('This name is not valid.Please enter another name.')

    def verify_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is not valid.Please enter another name.')
