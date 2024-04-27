from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

class Config(object):
    UPLOAD_DIRECTORY = app.root_path + "/uploads/"
    SQLALCHEMY_DATABASE_URI = "postgresql:///uploadit_db"
    SECRET_KEY = "secret key"

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes import home_page, download_page, upload_page, favicon_page

app.register_blueprint(home_page)
app.register_blueprint(download_page)
app.register_blueprint(upload_page, url_prefix="/upload")
app.register_blueprint(favicon_page)

import uploadit.routes as routes
import uploadit.models as models

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1212, debug=True)