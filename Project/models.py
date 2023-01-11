from flask_login import UserMixin
from Project import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(40), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True, nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column("Password", db.String(60), unique=True, nullable=False)
    patients = db.relationship("Patients", backref="planner")



# Create Patient Model
class Patients(db.Model):
    __tablename__ = "Patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(80), nullable=False)
    surname = db.Column("surname", db.String(80), nullable=False)
    email = db.Column("email", db.String(80), nullable=False)
    phone = db.Column("phone", db.String(20), nullable=False)
    relationship = db.Column("relationship", db.String(120), nullable=False)
    treatment = db.Column("treatment", db.Text, nullable=False)
    date_posted = db.Column("date", db.DateTime, default = datetime.utcnow)
    #Foreign key to link users
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="planner")

class Notes(db.Model):
    __tablename__ = "Notes"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column("sender", db.String(80), nullable=False)
    receiver = db.Column("receiver", db.String(80), nullable=False)
    notes = db.Column("notes", db.Text, nullable=False)
    date_posted = db.Column("date", db.DateTime, default = datetime.utcnow)
    #Foreign key to link users
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")
