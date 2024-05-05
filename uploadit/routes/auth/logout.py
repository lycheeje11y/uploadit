from flask import url_for, flash, redirect
from flask_login import current_user, logout_user
from . import auth

@auth.route('/logout')
def logout():
    flash(f'See ya, {current_user.username}', 'alert')
    logout_user()
    return redirect(url_for('auth.login'))