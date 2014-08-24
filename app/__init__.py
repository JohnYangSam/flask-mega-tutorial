from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Basic app configuration
app = Flask(__name__)
app.config.from_object('config')

# Database setup
# The rest is stored in modules
db = SQLAlchemy(app)

# Setup OpenID login
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# Need to import these for the flask app to
# access them
from app import views, models
