from db import db

class Goal(db.Model):  # ✅ This part is crucial
    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.00)
    deadline = db.Column(db.Date, nullable=False)

    # Optional: method to fetch goals by user
    @staticmethod
    def get_all_goals(user_id):
        return Goal.query.filter_by(user_id=user_id).all()
