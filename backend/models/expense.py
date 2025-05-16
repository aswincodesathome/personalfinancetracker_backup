from db import db
from datetime import date

class Expense(db.Model):
    __tablename__ = 'expenses'

    expense_id = db.Column(db.Integer, primary_key=True)  # ✅ Match DB
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    spent_on = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer)  # Optional: Add ForeignKey if needed
    payment_method_id = db.Column(db.Integer)  # Optional: Add ForeignKey if needed

    def __repr__(self):
        return f"<Expense {self.amount}>"
