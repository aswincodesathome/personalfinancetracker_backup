from flask import Blueprint, request, jsonify
from config import get_db_connection
import mysql.connector

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budget', methods=['POST'])
def add_budget():
    data = request.get_json()
    user_id = data.get('user_id')
    category_id = data.get('category_id')
    amount = data.get('amount')
    month = data.get('month')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO budget (user_id, category_id, amount, month)
            VALUES (%s, %s, %s, %s)
        """, (user_id, category_id, amount, month))
        
        conn.commit()
        return jsonify({"message": "Budget added successfully!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@budget_bp.route('/budget/<int:user_id>', methods=['GET'])
def get_user_budgets(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT b.budget_id, b.amount, b.month, c.name AS category
            FROM budget b
            JOIN category c ON b.category_id = c.category_id
            WHERE b.user_id = %s
        """, (user_id,))
        
        budgets = cursor.fetchall()
        return jsonify(budgets)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
@budget_bp.route('/budget/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    data = request.get_json()
    amount = data.get('amount')

    if amount is None:
        return jsonify({'error': 'Amount is required for update'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM budget WHERE budget_id = %s", (budget_id,))
        if cursor.fetchone() is None:
            return jsonify({'message': 'Budget not found.'}), 404

        cursor.execute("UPDATE budget SET amount = %s WHERE budget_id = %s", (amount, budget_id))
        conn.commit()
        return jsonify({'message': 'Budget updated successfully!'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@budget_bp.route('/budget/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM budget WHERE budget_id = %s", (budget_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Budget not found."}), 404

        return jsonify({"message": "Budget deleted successfully!"})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    finally:
        cursor.close()
        conn.close()
