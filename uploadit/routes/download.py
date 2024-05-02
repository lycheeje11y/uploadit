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
                    abort(500)
                    return redirect(url_for("download.download"))
                print(file.secure_filename)
                return send_from_directory(
                    upload_dir,
                    file.secure_filename,
                    as_attachment=True,
                    download_name=file.filename,
                )
            else:
                flash("Incorrect Filekey", 'error')
                return redirect(url_for('download.download'))
        else:
            return abort(422)
    elif request.method == "GET":
        query = db.session.query(File)
        results = db.session.scalars(query).all()
    return render_template("download.html", files=results)
