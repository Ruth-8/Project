from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, logout_user, login_user, login_required
from Project.users.forms import RegistrationForm, LoginForm, UserUpdateForm
from Project.models import User
from Project.users.utils import save_picture
from Project import db, bcrypt


users = Blueprint('users', __name__)

@users.route("/registration", methods=['GET', 'POST'])
def registration():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!', 'success')
        return redirect(url_for('main.index'))
    return render_template('registration.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash("You entered an invalid Login Name and/or Password combination. Please verify that you entered this information correctly!", 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    form = UserUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.picture = picture
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Was Updated!', 'success')
        return redirect(url_for('users.user'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    picture = url_for('static', filename='pictures/' + current_user.picture)
    return render_template('user.html', title='Account', form=form, picture=picture)
