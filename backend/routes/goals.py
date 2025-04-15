from flask import Blueprint, request, jsonify
from config import get_db_connection
import mysql.connector

goals_bp = Blueprint('goals', __name__)

# 1. Add new goal
@goals_bp.route('/goals', methods=['POST'])
def add_goal():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    target_amount = data.get('target_amount')
    deadline = data.get('deadline')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO goals (user_id, title, target_amount, deadline)
            VALUES (%s, %s, %s, %s)
        """, (user_id, title, target_amount, deadline))
        conn.commit()
        return jsonify({"message": "Goal added successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 2. Get all goals for a user
@goals_bp.route('/goals/<int:user_id>', methods=['GET'])
def get_goals(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT goal_id, title, target_amount, current_amount, deadline
            FROM goals
            WHERE user_id = %s
        """, (user_id,))
        goals = cursor.fetchall()
        return jsonify(goals)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 3. Update current amount for a goal
@goals_bp.route('/goals/<int:goal_id>', methods=['PUT'])
def update_goal_progress(goal_id):
    data = request.get_json()
    current_amount = data.get('current_amount')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE goals
            SET current_amount = %s
            WHERE goal_id = %s
        """, (current_amount, goal_id))
        conn.commit()
        return jsonify({"message": "Goal updated successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 4. Delete a goal
@goals_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM goals WHERE goal_id = %s", (goal_id,))
        conn.commit()
        return jsonify({"message": "Goal deleted successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
