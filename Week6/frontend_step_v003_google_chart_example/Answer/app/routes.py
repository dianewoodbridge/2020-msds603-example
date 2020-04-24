from app import application, classes, db
from flask import flash, render_template, redirect, request, Response, url_for
from flask_login import current_user, login_user, login_required, logout_user
import boto3

from app.plotly_example import plotly_map

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



@application.route('/list')
@login_required
def list():
    bucket_name = 'msds603'
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    unsorted_keys = []

    for object_summary in my_bucket.objects.filter():
        unsorted_keys.append([object_summary.key, object_summary.last_modified.strftime("%Y-%m-%d %H:%M:%S")])

    return render_template('list.html', items=unsorted_keys, authenticated_user=current_user.is_authenticated)



@application.route('/download/<key>')
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



@application.route('/progress_example', methods=('GET', 'POST'))
@login_required
def progress_example():
    return render_template('progress_example.html', progress=50)


@application.route('/javascript_example', methods=('GET', 'POST'))
@login_required
def javascript_example():
    locations = classes.Location.query.all()
    location_form = classes.LocationForm()
    if location_form.validate_on_submit():
        name = location_form.name.data
        details = location_form.details.data
        longitude = location_form.longitude.data
        latitude = location_form.latitude.data

        location_count = classes.Location.query.filter_by(name=name).count()
        if (location_count > 0):
            flash("Location name already exist.")
        else:
            location = classes.Location(name, longitude, latitude,  details)
            db.session.add(location)
            db.session.commit()
        return redirect(url_for('javascript_example'))

    return render_template('javascript_example.html', locations=locations, location_form = location_form)


@application.route('/update_location',  methods=['GET', 'POST'])
@login_required
def update_code():
    data = request.get_json(force=True)

    location_name = data['button_name']

    location = classes.Location.query.filter_by(name=location_name).first()
    db.session.delete(location)
    db.session.commit()

    #return redirect(url_for('javascript_example'))
    return "deleted"


@application.route('/plotly_example', methods=('GET', 'POST'))
@login_required
def plotly_example():
    locations = classes.Location.query.all()
    output = plotly_map(locations)
    return render_template('plotly_map.html', source=output)

@application.route('/google_example')
@login_required
def google_example():
    query = classes.Fertility.query.all()
    result = []
    for row in query :
        result.append([row.id, row.life_expectancy, row.fertility_rate, row.region, row.population])
        
    return render_template('google_chart.html', lines=result)
    