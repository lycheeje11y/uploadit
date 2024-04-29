from flask import Blueprint, render_template
from flask_login import login_required
from uploadit import db
from uploadit.models import File

browse_page = Blueprint("browse", __name__)

@browse_page.route('/browse')
@login_required
def browse():
    query = db.session.query(File)
    results = db.session.scalars(query).all()
    return render_template("browse.html", files=results)