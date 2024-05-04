import os
import uploadit

class Config(object):
    # MAIL STUFF
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    
    SECRET_KEY = 'THIS IS MY SECRET KEY'


    try:
        if os.getenv("IS_DOCKER") == "yes":
            SQLALCHEMY_DATABASE_URI = (
                "postgresql://postgres:password@db:5432/uploadit_db"
            )
        else:
            SQLALCHEMY_DATABASE_URI = "postgresql:///uploadit_db"
    except:
        SQLALCHEMY_DATABASE_URI = "postgresql:///uploadit_db"

        
