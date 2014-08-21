#!/Users/johnys/.virtualenvs/main/bin/python

""" Script to run and manage the flask app run 'manage.py' for details """

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os.path

from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

"""
Old run.py script that this replaces:

#!/Users/johnys/.virtualenvs/main/bin/python
from app import app
app.run(debug = True)
"""