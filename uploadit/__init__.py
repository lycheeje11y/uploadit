from logging.handlers import SMTPHandler, RotatingFileHandler
import sqlalchemy as sa
import sqlalchemy.orm as so
import logging
import os

from flask import Flask
app = Flask(__name__)



# CONFIG
from uploadit.config import Config
config = Config
app.config.from_object(config)

from dotenv import load_dotenv
load_dotenv()
app.config["UPLOAD_DIRECTORY"] = os.getcwd() + '/uploads/'

from uploadit.log import LogType
app.config["LOG"] = LogType.FILE

if os.getenv("LOG_TYPE") == 'MAIL':
    app.config["LOG"] = LogType.MAIL

from flask_mail import Mail
mail = Mail(app)

from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager


from uploadit.database import db
from uploadit.routes import *


# INITIATE APP





# CORS
CORS(app)

# DEBUG
from uploadit.models import File, User
db.init_app(app)
migrate = Migrate(app, db)


if not app.debug:
    if app.config["LOG"] == LogType.FILE:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/uploadit.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('UploadIt startup')
    elif app.config["LOG"] == app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='UploadIT Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

# LOGIN
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# BLUPRINTS
app.register_blueprint(home_page)
app.register_blueprint(download_page, url_prefix='/download')
app.register_blueprint(upload_page, url_prefix='/upload')
app.register_blueprint(auth, url_prefix='/u')
app.register_blueprint(favicon_page)


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'mail': mail, 'User': User, 'File': File}
