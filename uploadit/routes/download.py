from flask import (
    Blueprint,
    request,
    abort,
    flash,
    redirect,
    send_from_directory,
    render_template,
    current_app,
    url_for,
)
from uploadit import db
from uploadit.models import File

import sqlalchemy as sa
import sqlalchemy.orm as so

download_page = Blueprint("download", __name__)


@download_page.route("/", methods=["POST", "GET"])
def download():
    if request.method == "POST":
        data = request.form
        requested_key = data.get("download_id")
        if requested_key != None:
            query = sa.select(File.filekey)
            valid_key_list = db.session.scalars(query).all()
            if requested_key in valid_key_list:
                upload_dir = current_app.config["UPLOAD_DIRECTORY"]
                query = sa.select(File).where(File.filekey == requested_key)
                file = db.session.scalar(query)
                if file is None:
                    flash("Incorrect Filekey")
                    return redirect(url_for("download.download"))
                return send_from_directory(
                    upload_dir,
                    file.secure_filename,
                    as_attachment=True,
                    download_name=file.filename,
                )
            else:
                return abort(403)
        else:
            return abort(422)
    elif request.method == "GET":
        return render_template("download.html")
