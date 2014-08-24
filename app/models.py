from app import db
from passlib.apps import custom_app_context as pwd_context

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # True if the user is allowed to authenticate
    def is_authenticated(self):
        return True

    # True if the user is active (not banned / inactive)
    def is_active(self):
        return True

    # Only True for fake users that should not log in
    def is_anonymous(self):
        return True

    # Needs to return a UID for the user in unicode format
    def get_id(self):
        return unicode(self.id)

    # Tells how to print objects of the class
    def __repr__(self):
        return '<Usre %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr_(self):
        return '<Post %r>' % (self.body)
