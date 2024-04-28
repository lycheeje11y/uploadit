from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
)

home_page = Blueprint("index", __name__)
favicon_page = Blueprint("favicon", __name__)


@home_page.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@favicon_page.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="images/favicon.ico"))
