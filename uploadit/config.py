import os


class Config(object):
    SECRET_KEY = "secret key"
    try:
        if os.getenv("IS_DOCKER") == "yes":
            SQLALCHEMY_DATABASE_URI = (
                "postgresql://postgres:password@db:5432/uploadit_db"
            )
        else:
            SQLALCHEMY_DATABASE_URI = "postgresql:///uploadit_db"
    except:
        SQLALCHEMY_DATABASE_URI = "postgresql:///uploadit_db"
