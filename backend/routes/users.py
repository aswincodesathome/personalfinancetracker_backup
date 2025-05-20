from flask import Blueprint, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models.user import User
from models.expense import Expense
from models.income import Income

users_bp = Blueprint('users', __name__, template_folder='../../frontend/templates')

# ✅ GET login page
@users_bp.route('/login', methods=['GET'])
def login_get():
    return render_template('login_signup.html')

# ✅ POST login logic
@users_bp.route('/login', methods=['POST'])
def login_post():
    data = request.form or request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        session['user_name'] = user.full_name
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password!"}), 401

# ✅ GET signup page
@users_bp.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html')

# ✅ POST signup logic
@users_bp.route('/signup', methods=['POST'])
def signup_post():
    data = request.form or request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age')
    working_status = data.get('working_status')

    # Check if email already used
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"success": False, "message": "Email already registered!"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        age=age,
        working_status=working_status
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": True, "message": "Account created successfully!"})
    except Exception as e:
        db.session.rollback()
        print("Signup error:", e)
        return jsonify({"success": False, "message": f"Signup failed: {str(e)}"}), 500

# ✅ Dashboard route
@users_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return render_template('login_signup.html')  # Redirect to login if not logged in

    user_id = session['user_id']
    user_name = session.get('user_name', 'User')

    # Total Income
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.00

    # Total Expense
    total_expense = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.00

    # Balance
    balance = total_income - total_expense

    return render_template('dashboard.html',
                           total_income=f"{total_income:.2f}",
                           total_expense=f"{total_expense:.2f}",
                           balance=f"{balance:.2f}",
                           user_name=user_name,
                           user_id=user_id)

# ✅ GET user ID from session (for JS use in goals.html)
@users_bp.route('/get_user_id', methods=['GET'])
def get_user_id():
    if 'user_id' in session:
        return jsonify({"user_id": session['user_id']})
    return jsonify({"error": "Not logged in"}), 401

@users_bp.route('/chatbot')
def show_chatbot():
    return render_template('chatbot.html')
# ✅ Logout route
# ✅ Logout route
@users_bp.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')  # Or redirect to home if you want
