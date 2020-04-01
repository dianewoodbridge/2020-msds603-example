from app import application, classes, db
from flask import render_template, redirect, url_for

@application.route('/index')
@application.route('/')
def index():
    return("<h1> Hello World </h1>")

@application.route('/register',  methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data
        ##################################
        #### UPDATE THIS (EXERCISE 1) ####
        ##################################
        user = classes.User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=registration_form)
