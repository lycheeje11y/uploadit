from flask import (
    Blueprint,
    send_from_directory,
    abort,
    redirect,
    flash,
    url_for,
    render_template,
    request,
    current_app,
)
from werkzeug.utils import secure_filename
import sqlalchemy as sa
import sqlalchemy.orm as so
from uploadit import db
from uploadit.utils import random_string
from uploadit.models import File
from pathlib import Path
import os

home_page = Blueprint("index", __name__)
download_page = Blueprint("download", __name__)
upload_page = Blueprint("upload", __name__)
favicon_page = Blueprint("favicon", __name__)

@home_page.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@download_page.route("/download", methods=["POST", "GET"])
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
                    return redirect(url_for('download.download'))
                return send_from_directory(upload_dir, file.secure_filename, as_attachment=True, download_name=file.filename)
            else:
                return abort(403)
        else:
            return abort(422)
    elif request.method == "GET":
        return render_template("download.html")

@upload_page.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files["file"]
        except KeyError:
            return "No file chosen", 422

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
            print(f'Error: {e}')
            return "Error saving file.", 500

        total_chunks = int(request.form["dztotalchunkcount"])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
                return "Size mismatch.", 500

        key = random_string()
        data = File(filekey=key, filename=file.filename, secure_filename=secure_filename_var)
        db.session.add(data)
        db.session.commit()

        flash(f'Upload Complete. The file {secure_filename_var} has been saved with the key {key}')
        return "Upload Completed", 200
    
    elif request.method == 'GET':
        return render_template('upload.html')

@favicon_page.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="images/favicon.ico"))

