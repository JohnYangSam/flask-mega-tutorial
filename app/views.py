from flask import (render_template, flash, redirect, session, url_for, request, g)
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

# Homepage
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


# Login

# Functions with this decorator are run each time a request is received
# before the view function
@app.before_request
def before_request():
    # current_user returns the current user for the request (flask login)
    # we add it to 'g' to have an easier handle to it in things like templates
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    # 'g' is the place to store & share data through the lifecycle of a request
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # session stores data for any future requests of the client
        # flask keeps a session file for each application client
        session['remember_me'] = form.remember_me.data
        nickname = form.nickname.data
        password = form.password.data
        email = form.email.data

        # Checking basics
        if nickname is None or nickname == "":
            form.errors.nickname.append('Must enter a nickname')
            return redirect(url_for('login'))
        if password is None:
            form.errors.password.append("Must enter a password")
            return redirect(url_for('login'))

        # Check if login / registration
        user = User.query.filter_by(nickname=nickname).first()
        if user is None:
            if (email is None or email == ""):
                flash('Please enter a valid email to register')
                return redirect(url_for('login'))

            user = User(nickname=nickname,
                        email=email,
                        role=ROLE_USER)
            db.session.add(user)
            db.session.commit()

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        # 'next' request arg is automatically set by flask login when
        # @lm.login_required decorator is used
        return redirect(request.args.get('next') or url_for('index'))


        # TODO: Put back
        #return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPEN_ID_PROVIDERS'])


# Login logic
@lm.user_loader
def load_user(id):
    # Flask-Login ids are unicode strings, hence conversion
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    # 'next' request arg is automatically set by flask login when
    # @lm.login_required decorator is used
    return redirect(request.args.get('next') or url_for('index'))
