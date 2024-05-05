from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user
import sqlalchemy as sa
from uploadit.forms import ResetPasswordForm
from uploadit.models import User
from uploadit import db
from . import user_routes

@user_routes.route('reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'alert')
        return redirect(url_for('index.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token verification failed', 'error')
        return redirect(url_for('index.index'))
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        print("token_validated")
        user.set_password(form.password.data)
        db.session.commit()
        flash('You password has been reset', 'alert')

        return redirect(url_for('users.login'))
    
    return render_template('users/reset_password/reset_password.html', form=form)