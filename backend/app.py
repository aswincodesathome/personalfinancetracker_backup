import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, session, jsonify  # Added jsonify import
from flask_cors import CORS
from flask_migrate import Migrate
from db import db

from models import user, income, expense, goal

# Blueprints
from routes.users import users_bp
from routes.expenses import expenses_bp
from routes.income import income_bp
from routes.budget import budget_bp
from routes.goals import goals_bp
from routes.categories import categories_bp
from routes.payment_methods import payment_bp
from routes.summary import summary_bp
from routes.analytics import analytics_bp

# Flask app setup
app = Flask(__name__, template_folder='../frontend/templates')
CORS(app)
app.secret_key = "supersecretkey"

# ✅ Correct MySQL URI with special character handling
# If your password has @, :, or other symbols, encode them properly using urllib.parse
from urllib.parse import quote_plus
password = quote_plus("root@123")  # This safely escapes the password

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root%40123@localhost/finance_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'root@123'
app.config['DB_NAME'] = 'finance_tracker'


# Initialize DB and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(expenses_bp, url_prefix="/expenses")
app.register_blueprint(income_bp, url_prefix="/income")
app.register_blueprint(budget_bp)
app.register_blueprint(goals_bp, url_prefix='/goals')
app.register_blueprint(categories_bp, url_prefix="/categories")
app.register_blueprint(payment_bp)
app.register_blueprint(summary_bp)  
app.register_blueprint(analytics_bp, url_prefix="/analytics")

# Test route
@app.route('/')
def home():
    return '🎉 Personal Finance Tracker Backend is Running with MySQL! 🎉'

@app.route('/get_user_id')
def get_user_id():
    if 'user_id' in session:
        return jsonify({'user_id': session['user_id']})
    else:
        return jsonify({'error': 'Not logged in'}), 401

if __name__ == "__main__":
    app.run(debug=True)
