from flask import Flask
from flask_cors import CORS
from db import db
from routes.users import users_bp
from routes.expenses import expenses_bp
from config import get_db_connection

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register the users and expenses blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(expenses_bp)

@app.route('/')
def home():
    return '🎉 Personal Finance Tracker Backend is Running! 🎉'

if __name__ == "__main__":
    app.run(debug=True)
