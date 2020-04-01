from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Initialization
# Create an application instance (an object of class Flask)  which handles all requests.
application = Flask(__name__)
application.config.from_object(Config)

db = SQLAlchemy(application)
db.create_all()
db.session.commit()


