from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from logging.handlers import SMTPHandler
from uploadit.config import Config
from uploadit.database import db
from uploadit.routes import *
import sqlalchemy as sa
import sqlalchemy.orm as so
import os
import logging


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_DIRECTORY"] = os.getcwd() + "/uploads/"
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    from uploadit.models import File, User

    migrate = Migrate(app, db)
    mail = Mail(app)

    from uploadit.routes import home_page, download_page, upload_page, favicon_page

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    app.register_blueprint(home_page)
    app.register_blueprint(download_page, url_prefix='/download')
    app.register_blueprint(upload_page, url_prefix='/upload')
    app.register_blueprint(user_routes, url_prefix='/u')
    app.register_blueprint(favicon_page)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'so': so, 'db': db, 'mail': mail, 'User': User, 'File': File}

    return app
