from utils import random_string, get_config
from flask import (
    Flask,
    Blueprint,
    send_file,
    abort,
    redirect,
    url_for,
    render_template,
    request,
    current_app,
)
from werkzeug.utils import secure_filename
from pathlib import Path
import json
import os

home_page = Blueprint("index", __name__)
download_page = Blueprint("download", __name__)
upload_page = Blueprint("upload", __name__)
favicon_page = Blueprint("favicon", __name__)

json_db = get_config()
print(json_db)

@home_page.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@download_page.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "POST":
        data = request.form
        requested_id = data.get("download_id")
        if requested_id != None:
            valid_id_list = json_db.keys()
            print(valid_id_list)
            if requested_id in valid_id_list:
                upload_dir = current_app.config["UPLOAD_DIRECTORY"]
                return_file = f'{upload_dir}{json_db[requested_id]}'
                return send_file(return_file, as_attachment=True)
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
        filename = f"{file_uuid[:8]}_{secure_filename(file.filename)}"
        save_path = Path(current_app.config["UPLOAD_DIRECTORY"], filename)
        print(save_path)
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
            
        with open('files.json', 'r') as f:
            json_data = json.load(f)

        data = {f'{random_string()}': f'{filename}'}
        json_data.update(data)

        with open('files.json', 'w') as f:
            json.dump(json_data, f)
        return "Upload Completed", 200
    
    elif request.method == 'GET':
        return render_template('upload.html')

@favicon_page.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="images/favicon.ico"))

def serve():
    app = Flask(__name__)

    app.config["UPLOAD_DIRECTORY"] = app.root_path + "/uploads/"

    app.register_blueprint(home_page)
    app.register_blueprint(download_page)
    app.register_blueprint(upload_page, url_prefix="/upload")
    app.register_blueprint(favicon_page)

    return app.run(host="0.0.0.0", port="1212", debug=True)