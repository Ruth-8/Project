from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user
from Project.views.forms import PatientForm, NotesForm
from Project.models import Patients, Notes
from Project import db

views = Blueprint('views', __name__)

@views.route('/dashboard')
def posts():
    posts = Patients.query.order_by(Patients.date_posted)
    return render_template('dashboard.html', posts=posts)

@views.route('/dashboard/<int:id>')
def post(id):
    post = Patients.query.get(id)
    return render_template("patient.html", post=post)

@views.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    form = PatientForm()
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

@views.route('/dashboard/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Patients.query.get(id)
    form = PatientForm()
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
        return redirect(url_for('views.posts', id=post.id))
    form.name.data=post.name
    form.surname.data=post.surname
    form.email.data=post.email
    form.phone.data=post.phone
    form.relationship.data=post.relationship
    form.treatment.data=post.treatment
    return render_template("update.html", form=form)

@views.route('/dashboard/delete/<int:id>')
def delete(id):
    delete = Patients.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('views.posts'))

@views.route('/notes')
def notes():
    # get all notes in one place
    notes = Notes.query.order_by(Notes.date_posted)
    return render_template("notes.html", notes=notes)

@views.route('/notes/<int:id>')
def note(id):
    note = Notes.query.get(id)
    return render_template("note.html", note=note)

@views.route('/add_note', methods=['GET', 'POST'])
def add_notes():
    form = NotesForm()
    if form.validate_on_submit():
        note = Notes(sender=form.sender.data,receiver=form.receiver.data, notes=form.notes.data)
        # clear the form
        form.sender.data=''
        form.receiver.data=''
        form.notes.data=''
        db.session.add(note)
        db.session.commit()
        flash("Data Submitted Successfully!")
    return render_template("add_note.html", form=form)

@views.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note = Notes.query.get(id)
    form = NotesForm()
    if form.validate_on_submit():
        note.sender = form.sender.data
        note.receiver = form.receiver.data
        note.notes = form.notes.data
        # update database
        db.session.add(note)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('views.notes', id=note.id))
    form.sender.data=note.sender
    form.receiver.data=note.receiver
    form.notes.data=note.notes
    return render_template("edit.html", form=form)

@views.route('/notes/delete/<int:id>')
def delete2(id):
    delete2 = Notes.query.get(id)
    db.session.delete(delete2)
    db.session.commit()
    return redirect(url_for('views.notes'))

