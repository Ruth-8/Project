import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
from datetime import datetime
import secrets
from PIL import Image
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register'
login_manager.login_message_category = 'info'

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(40), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True, nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column("Password", db.String(60), unique=True, nullable=False)
    # one to many relationship
    patients = db.relationship("Patients", backref="planner")
    notes = db.relationship("Notes")

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

class Notes(db.Model):
    __tablename__ = "Notes"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column("sender", db.String(80), nullable=False)
    receiver = db.Column("receiver", db.String(80), nullable=False)
    notes = db.Column("notes", db.Text, nullable=False)
    date_posted = db.Column("date", db.DateTime, default = datetime.utcnow)
    #Foreign key to link users
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    return User.query.get(int(user_id))


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!', 'success')
        return redirect(url_for('index'))
    return render_template('registration.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("You entered an invalid Login Name and/or Password combination. Please verify that you entered this information correctly!", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)

    output_size = (190, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    form = forms.UserUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.picture = picture
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Was Updated!', 'success')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    picture = url_for('static', filename='pictures/' + current_user.picture)
    return render_template('user.html', title='Account', form=form, picture=picture)


@app.route('/dashboard')
def posts():
    # get all the patients in dashboard
    posts = Patients.query.order_by(Patients.date_posted)
    return render_template("dashboard.html", posts=posts)

@app.route('/dashboard/<int:id>')
def post(id):
    post = Patients.query.get(id)
    return render_template("patient.html", post=post)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    form = forms.PatientForm()
    if form.validate_on_submit():
        planner = current_user.id
        patient = Patients(name = form.name.data, surname = form.surname.data, email = form.email.data, phone = form.phone.data,  relationship = form.relationship.data, treatment=form.treatment.data, user_id=planner)
        # clear the form
        form.name.data=''
        form.surname.data=''
        form.email.data=''
        form.phone.data=''
        form.relationship.data=''
        form.treatment.data=''
        db.session.add(patient)
        db.session.commit()
        flash("Data Submitted Successfully!")
    return render_template("add_patient.html", form=form)

@app.route('/dashboard/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Patients.query.get(id)
    form = forms.PatientForm()
    if form.validate_on_submit():
        post.name = form.name.data
        post.surname = form.surname.data
        post.email = form.email.data
        post.phone = form.phone.data
        post.relationship = form.relationship.data
        post.treatment = form.treatment.data
        # update database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('posts', id=post.id))
    form.name.data=post.name
    form.surname.data=post.surname
    form.email.data=post.email
    form.phone.data=post.phone
    form.relationship.data=post.relationship
    form.treatment.data=post.treatment
    return render_template("update.html", form=form)

@app.route('/dashboard/delete/<int:id>')
def delete(id):
    delete = Patients.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('posts'))


@app.route("/")
def index():
    return render_template("base.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    db.create_all()
