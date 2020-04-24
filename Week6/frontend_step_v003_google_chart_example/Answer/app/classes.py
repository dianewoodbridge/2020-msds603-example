from flask_login import UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import FloatField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from app import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Location(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    details = db.Column(db.String(500), nullable=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    def __init__(self, name, lon, lat, details):
        self.name = name
        self.longitude = lon
        self.latitude = lat
        self.details = details


class Fertility(db.Model):
    id = db.Column(db.String(80), primary_key = True)
    life_expectancy = db.Column(db.Integer, nullable = False)
    fertility_rate = db.Column(db.Float, nullable = False)
    region = db.Column(db.String(80), nullable = False)
    population = db.Column(db.Integer, nullable = False)

    def __init__(self, id, life_expectancy, fertility_rate, region, population):
        self.id = id
        self.life_expectancy = life_expectancy
        self.fertility_rate = fertility_rate
        self.region = region
        self.population = population

db.create_all()
db.session.commit()

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

class LocationForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    longitude = FloatField('Longitude:', validators=[DataRequired()])
    latitude = FloatField('Latitude:', validators=[DataRequired()])
    details = StringField('Details:')
    submit = SubmitField('Submit')


# user_loader :
# This callback is used to reload the user object
# from the user ID stored in the session.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
