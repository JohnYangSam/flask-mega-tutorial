"""
Configuration file for flask app
"""


# Flask WTF form configuration
CSRF_ENABLED = True
SECRET_KEY = "adskfjskS()#Jkl4"


# OpenID Configuration
OPEN_ID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

# Database Configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# The location of the SQLite file. Make sure you have the correct
# number of '/' (slashes)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')
