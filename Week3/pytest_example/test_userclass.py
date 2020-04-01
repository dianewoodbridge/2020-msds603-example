from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Initialization
# Create an application instance (an object of class Flask)  which handles all requests.
application = Flask(__name__)
application.config.from_object(Config)

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy(application)
db.create_all()
db.session.commit()

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'week3.db')

class User(db.Model):
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

def UserFromDB(username):
    user = User.query.filter_by(username=username).first()
    return user

def test_UserFromDB():
    # Assuming that "diane, diane@gmail.com, 1234" is always in the database
    # Good to have a test user account
    assert UserFromDB("diane").email == "diane@gmail.com"
    assert UserFromDB("diane").username == "diane"
    assert UserFromDB("diane").check_password("1234") == True
