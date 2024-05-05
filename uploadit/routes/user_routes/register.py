from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user
import sqlalchemy as sa
from uploadit.forms import RegistrationForm
from uploadit.models import User
from uploadit import db
from . import user_routes

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
    
    return render_template('users/register.html', form=form)