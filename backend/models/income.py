from db import db
from datetime import datetime

class Income(db.Model):
    __tablename__ = 'income'

    income_id = db.Column(db.Integer, primary_key=True)  # ✅ Match DB
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    source = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    received_on = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Income {self.amount} - {self.source}>"
