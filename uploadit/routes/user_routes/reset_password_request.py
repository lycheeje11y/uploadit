from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user
import sqlalchemy as sa
from uploadit.forms import ResetPasswordRequestForm
from uploadit.email import send_password_reset_email
from uploadit.models import User
from uploadit import db
from . import user_routes

@user_routes.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'alert')
        return redirect(url_for('index.index'))
    form = ResetPasswordRequestForm(request.form)
    if form.validate_on_submit and request.method == 'POST':
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'alert')
        return redirect(url_for('users.login'))
    
    return render_template('users/reset_password/reset_password_request.html', form=form)
