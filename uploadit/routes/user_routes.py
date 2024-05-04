from flask import render_template, Blueprint, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from uploadit.forms import LoginForm, RegistrationForm
from uploadit.models import User
from uploadit import db

user_routes = Blueprint("users", __name__)

@user_routes.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.username}', 'alert')
        return redirect(url_for('index.index'))

    return render_template("login.html", form=form)

@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'alert')
        return redirect(url_for('index.index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to the uploadit community, {user.username}', 'alert')
        login_user(user)
        return redirect(url_for('index.index'))
    elif not form.validate_email:
        return "Invalid Email Address", 500
    
    return render_template('register.html', form=form)

@user_routes.route('/logout')
def logout():
    flash(f'See ya, {current_user.username}', 'alert')
    logout_user()
    return redirect(url_for('users.login'))

@user_routes.route('/profile')
def profile():
    pass
