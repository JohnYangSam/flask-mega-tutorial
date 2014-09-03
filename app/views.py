from flask import (render_template, flash, redirect, session, url_for, request, g)
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, RegistrationForm
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
def login():
    # 'g' is the place to store & share data through the lifecycle of a request
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Successfully logged in as %s' % form.user.username)
        # session stores data for any future requests of the client
        # flask keeps a session file for each application client

        session['remember_me'] = form.remember_me.data
        # Setup the remember_me from the session
        # TODO: what exactly this is doing
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            # dict.pop(key, default) removes the key and ret val or default
            session.pop('remember_me', None)

        login_user(form.user, remember=remember_me)
        # 'next' request arg is automatically set by flask login when
        # @lm.login_required decorator is used
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 'g' is the place to store & share data through the lifecycle of a request
    if g.user is not None and g.user.is_authenticated():
        flash('You are already logged in. Log out to create a new account.')
        return redirect(request.args.get('next') or url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # session stores data for any future requests of the client
        # flask keeps a session file for each application client

        username = form.username.data
        email = form.email.data
        password = form.password.data

        # All checks have passed = create a new user
        user = User(username=username,
                    email=email,
                    role=ROLE_USER)
        user.hash_password(password)

        db.session.add(user)
        db.session.commit()

        # TODO: Errors commiting? This may be repetitive
        # get ther user again
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("There was an error registering.")
            return redirect(url_for('register'))

        # Setup the remember_me from the session
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)

        print("Should redirect to main")
        return redirect(request.args.get('next') or url_for('index'))

    print("Should be going back to register")
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))


# Login logic
@lm.user_loader
def load_user(id):
    # Flask-Login ids are unicode strings, hence conversion
    return User.query.get(int(id))
