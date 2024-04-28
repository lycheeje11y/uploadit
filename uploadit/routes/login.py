from flask import render_template, Blueprint, url_for, flash, redirect, request
from uploadit.forms import LoginForm

login_page = Blueprint("login", __name__)

@login_page.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        flash(f'Login requested for {form.username.data} with password {form.password.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('login.login'))

    return render_template("login.html", form=form)
