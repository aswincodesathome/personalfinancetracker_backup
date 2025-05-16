from flask import Blueprint, jsonify, render_template
from config import get_db_connection
import mysql.connector

summary_bp = Blueprint('summary', __name__, template_folder='../../frontend/templates')

@summary_bp.route('/summary/history/<int:user_id>', methods=['GET'])
def get_full_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # ✅ Get all income entries
        cursor.execute("""
            SELECT 
                received_on AS date,
                'Income' AS type,
                source AS category,
                amount,
                '' AS description,
                '' AS payment_method
            FROM income
            WHERE user_id = %s
        """, (user_id,))
        income_data = cursor.fetchall()

        # ✅ Get all expense entries with category + payment method
        cursor.execute("""
            SELECT 
                spent_on AS date,
                'Expense' AS type,
                c.name AS category,
                e.amount,
                e.description,
                pm.method_name AS payment_method
            FROM expenses e
            JOIN category c ON e.category_id = c.category_id
            JOIN payment_method pm ON e.payment_method_id = pm.payment_method_id
            WHERE e.user_id = %s
        """, (user_id,))
        expense_data = cursor.fetchall()

        # ✅ Merge & sort
        combined = income_data + expense_data
        combined.sort(key=lambda x: x['date'], reverse=True)

        return render_template('summary.html', history=combined)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()
