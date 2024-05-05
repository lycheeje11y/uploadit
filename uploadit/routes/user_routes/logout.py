from flask import url_for, flash, redirect
from flask_login import current_user, logout_user
from . import user_routes

@user_routes.route('/logout')
def logout():
    flash(f'See ya, {current_user.username}', 'alert')
    logout_user()
    return redirect(url_for('users.login'))