from .utils import random_string, get_config
from flask import (
    Flask,
    Blueprint,
    send_file,
    abort,
    redirect,
    url_for,
    render_template,
    request,
)
from pathlib import Path
import json
import os

app = Flask(__name__)
files = get_config()
home_page = Blueprint("home", __name__)
favicon_page = Blueprint("favicon", __name__)
download_page = Blueprint("download", __name__)

@home_page.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@download_page.route("/download", methods=["POST"])
def download():
    if request.method == "POST":
        data = request.form
        requested_id = data.get("download_id")
        if requested_id != None:
            print("is none")
            valid_id_list = files.keys()

            if requested_id in valid_id_list:
                print("yess")
                return send_file(files[requested_id], as_attachment=True)
            else:
                return abort(403)
        else:
            return abort(422)

@favicon_page.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="images/favicon.ico"))

def serve():
    app.register_blueprint(home_page)
    app.register_blueprint(favicon_page)
    app.register_blueprint(download_page)

    return app.run(host="0.0.0.0", port="1212", debug=True)