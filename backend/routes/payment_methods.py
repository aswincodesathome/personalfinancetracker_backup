from flask import Blueprint, request, jsonify
from config import get_db_connection
import mysql.connector

payment_bp = Blueprint('payment_methods', __name__)

# POST – Add payment method
@payment_bp.route('/payment-methods', methods=['POST'])
def add_payment_method():
    data = request.get_json()
    user_id = data.get('user_id')
    method_name = data.get('method_name')
    card_number = data.get('card_number')
    expiry_date = data.get('expiry_date')
    bank_name = data.get('bank_name')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO payment_methods 
            (user_id, method_name, card_number, expiry_date, bank_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, method_name, card_number, expiry_date, bank_name))
        conn.commit()
        return jsonify({"message": "Payment method added successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# GET – All payment methods for a user
@payment_bp.route('/payment-methods/<int:user_id>', methods=['GET'])
def get_payment_methods(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM payment_methods WHERE user_id = %s
        """, (user_id,))
        methods = cursor.fetchall()
        return jsonify(methods)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
@payment_bp.route('/payment_methods/<int:method_id>', methods=['DELETE'])
def delete_payment_method(method_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM payment_methods WHERE method_id = %s", (method_id,))
        conn.commit()
        return jsonify({"message": "Payment method deleted successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
