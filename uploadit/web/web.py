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
    jsonify,
)
from werkzeug.utils import secure_filename
from pathlib import Path
import secrets
import os

home_page = Blueprint("index", __name__)
download_page = Blueprint("download", __name__)
upload_page = Blueprint("upload", __name__)
favicon_page = Blueprint("favicon", __name__)

files = get_config()

@home_page.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@download_page.route("/download", methods=["POST", "GET"])
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
    elif request.method == "GET":
        return render_template("download.html")

@upload_page.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files["file"]
            print(file)
        except KeyError:
            return "No file chosen", 422
        print(request.form)
        file_uuid = request.form["dzuuid"]
        # Generate a unique filename to avoid overwriting using 8 chars of uuid before filename.
        filename = f"{file_uuid[:8]}_{secure_filename(file.filename)}"
        save_path = Path("uploads", filename)
        current_chunk = int(request.form["dzchunkindex"])

        if not os.path.exists(save_path):

            print(os.listdir())
            f = open(filename, "w")
            f.close()
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

        return "Chunk upload successful.", 200

    elif request.method == 'GET':
        return render_template('upload.html')

@favicon_page.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="images/favicon.ico"))

def serve():
    app = Flask(__name__)

    app.register_blueprint(home_page)
    app.register_blueprint(download_page)
    app.register_blueprint(upload_page)
    app.register_blueprint(favicon_page)

    return app.run(host="0.0.0.0", port="1212", debug=True)