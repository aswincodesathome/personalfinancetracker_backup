from flask import Blueprint, request, jsonify
from config import get_db_connection
import mysql.connector

income_bp = Blueprint('income', __name__)

# ✅ Add new income
@income_bp.route('/income/<int:user_id>', methods=['POST'])
def add_income(user_id):
    data = request.get_json()
    source = data.get('source')
    amount = data.get('amount')
    received_on = data.get('received_on')  # Format: YYYY-MM-DD

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO income (user_id, source, amount, received_on)
            VALUES (%s, %s, %s, %s)
        """, (user_id, source, amount, received_on))

        conn.commit()
        return jsonify({"message": "Income added successfully!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# ✅ Get all incomes
@income_bp.route('/income/<int:user_id>', methods=['GET'])
def get_incomes(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT income_id, source, amount, received_on
            FROM income
            WHERE user_id = %s
            ORDER BY received_on DESC
        """, (user_id,))

        incomes = cursor.fetchall()
        return jsonify(incomes)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
