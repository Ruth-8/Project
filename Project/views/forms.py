from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

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







