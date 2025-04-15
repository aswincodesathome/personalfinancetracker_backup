from flask import Blueprint, jsonify, request
from config import get_db_connection
import mysql.connector

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/', methods=['POST'])
def add_expense():
    data = request.get_json()

    user_id = data.get('user_id')
    amount = data.get('amount')
    spent_on = data.get('spent_on')  # Should be YYYY-MM-DD format
    description = data.get('description')
    category_id = data.get('category_id')
    payment_method_id = data.get('payment_method_id')

    if not all([user_id, amount, spent_on, category_id, payment_method_id]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO expenses (user_id, amount, spent_on, description, category_id, payment_method_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, amount, spent_on, description, category_id, payment_method_id))
        
        conn.commit()
        return jsonify({"message": "Expense added successfully!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

# GET /expenses/<user_id> → List of expenses
@expenses_bp.route('/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                e.expense_id,
                e.amount,
                e.spent_on,
                e.description,
                c.name AS category,
                pm.method_name AS payment_method
            FROM expenses e
            JOIN category c ON e.category_id = c.category_id
            JOIN payment_methods pm ON e.payment_method_id = pm.method_id
            WHERE e.user_id = %s
            ORDER BY e.spent_on DESC
        """, (user_id,))
        
        expenses = cursor.fetchall()
        return jsonify(expenses)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    finally:
        cursor.close()
        conn.close()

# GET /expenses/summary/<user_id> → Total summary
@expenses_bp.route('/summary/<int:user_id>', methods=['GET'])
def get_total_expense_summary(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT SUM(amount) AS total_expense
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        return jsonify({
            "user_id": user_id,
            "total_expense": result['total_expense'] or 0.00
        })

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    finally:
        cursor.close()
        conn.close()
