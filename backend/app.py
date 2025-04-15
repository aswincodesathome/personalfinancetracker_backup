from flask import Flask
from flask_cors import CORS
from db import db
from routes.users import users_bp
from routes.expenses import expenses_bp
from routes.income import income_bp
from routes.budget import budget_bp
from routes.goals import goals_bp
from routes.categories import categories_bp
from routes.payment_methods import payment_bp
from config import get_db_connection
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register the users and expenses blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(expenses_bp, url_prefix='/expenses')
app.register_blueprint(income_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(categories_bp, url_prefix='/categories')
app.register_blueprint(payment_bp)

@app.route('/')
def home():
    return '🎉 Personal Finance Tracker Backend is Running! 🎉'

if __name__ == "__main__":
    app.run(debug=True)
