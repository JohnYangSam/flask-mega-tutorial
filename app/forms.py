"""
Microblog forms
"""

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms import validators
from app.models import User


# Form for Login
class LoginForm(Form):

    username = TextField('username', validators=[validators.Required()])
    password = PasswordField('password', validators=[validators.Required()])
    remember_me = BooleanField('remember_me', default=False)

    def __init(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        return_value = Form.validate(self)
        if not return_value:
            return False

        # username or email check
        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            user = User.query.filter_by(
                email=self.username.data).first()

        if user is None:
            self.username.errors.append(
                "Please enter a valid username or email.")
            return False

        # Password check
        if not user.verify_password(self.password.data):
            self.password.errors.append("Invalid password.")
            return False

        self.user = user
        return True


# Form for registration
class RegistrationForm(Form):

    username = TextField('username',
                         validators=[validators.Required(),
                                     validators.Length(min=4, max=25),
                                     validators.regexp("^[A-Za-z0-9_-]*$", message="Usernames can only have letters, numbers, _, and -")])

    email = TextField('email',
                      validators=[validators.Required(),
                                  validators.Email("Must be a valid email.")])

    password = PasswordField('password',
                             validators=[validators.Required(),
                                         validators.EqualTo('password_confirmation', message='Passwords must match')])

    password_confirmation = PasswordField('password_confirmation',
                                          validators=[validators.Required(message="Please enter a password confirmation")])

    accept_tos = BooleanField('I accept the TOS',
                              validators=[validators.Required()],
                              default="True")
    remember_me = BooleanField('remember_me', default=False)

    def __init(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        return_value = Form.validate(self)
        if not return_value:
            return False

        # username unique check
        user = User.query.filter_by(
            username=self.username.data).first()
        if user is not None:
            self.username.errors.append(
                "Sorry. That username is already taken.")
            return False

        # email unique check
        user = User.query.filter_by(
            email=self.email.data).first()
        if user is not None:
            self.email.errors.append(
                "That email is already taken by another user.")
            return False

        self.user = user
        return True
