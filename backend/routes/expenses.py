from flask import Blueprint, jsonify
from config import get_db_connection
import mysql.connector

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses/<int:user_id>', methods=['GET'])
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

@expenses_bp.route('/expenses/summary/<int:user_id>', methods=['GET'])
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
