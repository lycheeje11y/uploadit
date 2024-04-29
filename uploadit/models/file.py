import sqlalchemy as sa
from uploadit import db
import datetime

class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filekey = db.Column(db.String(50))
    filename = db.Column(db.String())
    secure_filename = db.Column(db.String())
    created_at = db.Column(sa.TIMESTAMP, default=datetime.datetime.now())

    def __init__(self, filekey, filename, secure_filename):
        self.filekey = filekey
        self.filename = filename
        self.secure_filename = secure_filename

    def __repr__(self):
        return f"<Filename: {self.filename}; secure_filename: {self.secure_filename}; key: {self.filekey}>"