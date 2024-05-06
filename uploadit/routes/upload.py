from flask import (
    Blueprint,
    request,
    flash,
    redirect,
    abort,
    render_template,
    current_app,
    url_for,
)
from flask_login import current_user, login_required
from uploadit import db
from uploadit.models import File
from uploadit.utils import random_string
from werkzeug.utils import secure_filename
from pathlib import Path
import os

import sqlalchemy as sa
import sqlalchemy.orm as so

upload_page = Blueprint("upload", __name__)


@upload_page.route("/", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        try:
            file = request.files["file"]
        except KeyError:
            return "No file chosen", 422

        is_public = request.form.get('is_public')
        if is_public == 'true':
            is_public = True
        elif is_public == 'false':
            is_public = False
        else:
            return "Bad Request", 422

        file_uuid = request.form["dzuuid"]
        # Generate a unique filename to avoid overwriting using 8 chars of uuid before filename.
        secure_filename_var = f"{file_uuid[:8]}_{secure_filename(file.filename)}"
        save_path = Path(current_app.config["UPLOAD_DIRECTORY"], secure_filename_var)
        current_chunk = int(request.form["dzchunkindex"])

        try:
            with open(save_path, "ab") as f:
                f.seek(int(request.form["dzchunkbyteoffset"]))
                f.write(file.stream.read())
        except OSError as e:
            print(f"Error: {e}")
            return "Error saving file.", 500

        total_chunks = int(request.form["dztotalchunkcount"])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
                return "Size mismatch.", 500
        
        key = random_string()
        data = File(
            filekey=key, filename=file.filename, secure_filename=secure_filename_var, uploader=current_user, is_public=is_public
        )
        db.session.add(data)
        db.session.commit()

        flash(
            f"Upload Complete. The file {secure_filename_var} has been saved with the key {key}", 'error'
        )
        return redirect(url_for("upload.upload"))

    elif request.method == "GET":
        return render_template("upload.html")
