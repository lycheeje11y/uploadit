from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user
import sqlalchemy as sa
from uploadit.forms import LoginForm
from uploadit.models import User
from uploadit import db
from . import user_routes


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

    return render_template("users/login.html", form=form)