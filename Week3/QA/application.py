from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_login import UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user, login_user, login_required, logout_user

basedir = os.path.abspath(os.path.dirname(__file__))

application = Flask(__name__)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join(basedir, 'week3.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(application)
login_manager = LoginManager()

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

@login_manager.user_loader
def load_user(id):  # id is the ID in User.
    return User.query.get(int(id))

@application.route('/login', methods=['GET', 'POST'])
def login():
    username = "diane"
    password = "1234"
    user = User.query.filter_by(username=username).first()
    print("current_user is {}".format(current_user))
    #print("current_user's username is {}".format(current_user.username))

    # Login and validate the user.
    if user is not None and user.check_password(password):
        login_user(user)
        print("current_user is {}".format(current_user))
        print("current_user's username is {}".format(current_user.username))
        return("<h1> Welcome {}!</h1>".format(username))

    return ("<h1> No one is logged in.")


if __name__ == '__main__':
    # login_manager needs to be initiated before running the app
    login_manager.init_app(application)
    # flask-login uses sessions which require a secret Key
    application.secret_key = os.urandom(24)

    # Create tables.
    db.create_all()
    db.session.commit()

    application.run(host='0.0.0.0', port=5000, debug=True)
