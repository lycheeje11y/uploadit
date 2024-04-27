from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from uploadit import db

class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filekey = db.Column(db.String(50))
    filename = db.Column(db.String())

    def __init__(self, filekey, filename):
        self.filekey = filekey
        self.filename = filename

    def __repr__(self):
        return f'The file "{self.filename}" has the key of "{self.filekey}"'