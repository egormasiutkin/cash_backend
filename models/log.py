from datetime import datetime

from . import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, nullable=False)
    pda_id = db.Column(db.String(50), nullable=True)
    employee_id = db.Column(db.Integer, nullable=True)
    manager_id = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
