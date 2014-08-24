"""
Microblog forms
"""


from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    # TODO: put back
    #openid = TextField('openid', validators=[Required()])
    openid = TextField('openid')
    remember_me = BooleanField('remember_me', default=False)

    nickname = TextField('nickname', validators=[Required()])
    password = TextField('password', validators=[Required()])
    email = TextField('email')
