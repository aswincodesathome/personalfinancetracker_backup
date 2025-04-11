from flask import Blueprint, request, jsonify
from db import db
from config import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])  # POST /users
def create_user():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age')
    working_status = data.get('working_status')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO users (full_name, email, password, age, working_status)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (full_name, email, password, age, working_status))
        conn.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/login', methods=['POST'])  # POST /users/login
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            return jsonify({'message': 'Login successful!', 'user': user}), 200
        else:
            return jsonify({'error': 'Invalid email or password!'}), 401
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()