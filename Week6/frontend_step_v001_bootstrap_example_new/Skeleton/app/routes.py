from app import application, classes, db
from flask import flash, render_template, redirect, Response, url_for
from flask_login import current_user, login_user, login_required, logout_user
import boto3

@application.route('/index')
@application.route('/')
def index():
    return render_template('index.html',
                           authenticated_user=current_user.is_authenticated)


@application.route('/register', methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count()
        + classes.User.query.filter_by(email=email).count()
        if(user_count > 0):
            flash('Error - Existing user : ' + username + ' OR ' + email)
            
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
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
            return redirect(url_for('examples'))
        else:
            flash('Invalid username and password combination!')
    return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.errorhandler(401)
def re_route(e):
    return redirect(url_for('login'))


@application.route('/examples', methods=['GET'])
@login_required
def examples():
    return render_template('examples_main.html', authenticated_user=current_user.is_authenticated)



@application.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    bucket_name = 'msds603'
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    unsorted_keys = []

    for object_summary in my_bucket.objects.filter():
        unsorted_keys.append([object_summary.key, object_summary.last_modified.strftime("%Y-%m-%d %H:%M:%S")])

    return render_template('list.html', items=unsorted_keys, authenticated_user=current_user.is_authenticated)



@application.route('/download/<key>', methods=['GET', 'POST'])
@login_required
def download(key):
    bucket_name = 'msds603'
    s3 = boto3.client('s3')
    file = s3.get_object(Bucket=bucket_name, Key=key)
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;" }
    )
    return redirect(url_for('list'))
