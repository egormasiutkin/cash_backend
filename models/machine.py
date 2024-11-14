from datetime import datetime

from . import db

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=True)
