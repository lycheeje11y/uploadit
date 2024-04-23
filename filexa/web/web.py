from web.utils import random_string
from flask import Flask, Blueprint, send_file, abort, request
from pathlib import Path
import os


class Config:
    def __init__(self):
        self.flask_app = Flask(__name__)
        self.base_directory = Path(os.getcwd())
        
        self.id = random_string()
        print(self.id)
        self.files = {f'{self.id}': "/Users/joey/projects/filexa/filexa/hello.txt"}

        home_page = Blueprint("home_page", __name__)
        print(self.files.keys())

        @home_page.route("/", defaults={"requested_id": None})
        @home_page.route("/<path:requested_id>")
        def index(requested_id):
            if requested_id:

                if requested_id in self.files.keys():
                    try:
                        return send_file(self.files[requested_id], as_attachment=True)
                    except FileNotFoundError:
                        return abort(404)
                else:   
                    return str(self.id)
            
            else:
                return "no path"
        self.flask_app.register_blueprint(home_page,)
