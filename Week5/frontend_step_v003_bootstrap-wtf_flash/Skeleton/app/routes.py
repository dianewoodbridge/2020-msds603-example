from app import application, classes, db
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

@application.route('/index')
@application.route('/')
def index():
    return render_template('index.html', authenticated_user=current_user.is_authenticated)

@application.route('/register',  methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
                     + classes.User.query.filter_by(email=email).count()
        if (user_count > 0):
            #### UPDATE THIS #####
            return '<h1>Error - Existing user : ' + username \
                   + ' OR ' + email + '</h1>'
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('register.html', form=registration_form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = classes.User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        #### UPDATE THIS -- Flash Message #####

    return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    #### UPDATE THIS #####
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout


@application.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret.html',
                           authenticated_user=current_user.is_authenticated,
                           name=current_user.username,
                           email=current_user.email)

#### ADD ERROR HANDLER  #####