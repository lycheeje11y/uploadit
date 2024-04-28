from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from uploadit.config import Config
from uploadit.database import db

import os

def serve():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config["UPLOAD_DIRECTORY"] =  os.getcwd() + "/uploads/"
    CORS(app, origins=["http://0.0.0.0:5000"])

    db.init_app(app)
    from uploadit.models import File
    migrate = Migrate(app, db)

    from uploadit.routes import home_page, download_page, upload_page, favicon_page
    app.register_blueprint(home_page)
    app.register_blueprint(download_page)
    app.register_blueprint(upload_page, url_prefix="/upload")
    app.register_blueprint(favicon_page)

    return app