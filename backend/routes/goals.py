from flask import Blueprint, render_template, request, redirect, jsonify, session
from models.goal import Goal
from models.expense import Expense
from models.income import Income
from db import db
from sqlalchemy import func

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')


# Route to render the main goals page with current balance
@goals_bp.route('/goals-page', methods=['GET'])
def goals_page():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    try:
        goals = Goal.get_all_goals(user_id)
        total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.00
        total_expense = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.00
        balance = total_income - total_expense
    except Exception:
        goals = []
        balance = 0.00

    return render_template('goals.html', user_id=user_id, goals=goals, balance=balance)


# API to fetch all goals for the logged-in user (with progress = current balance)
@goals_bp.route('/', methods=['GET'])
def get_goals():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    try:
        goals = Goal.get_all_goals(user_id)
        total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.00
        total_expense = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.00
        balance = total_income - total_expense

        goals_list = [{
            'goal_id': goal.goal_id,
            'title': goal.title,
            'target_amount': float(goal.target_amount),
            'deadline': goal.deadline.strftime('%Y-%m-%d'),
            'saved_amount': float(balance),  # This is balance
            'percent': round(min(balance / goal.target_amount * 100, 100), 1)  # Cap at 100%
        } for goal in goals]
        return jsonify(goals_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to add a new goal
@goals_bp.route('/', methods=['POST'])
def add_goal():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    title = data.get('title')
    target_amount = data.get('target_amount')
    deadline = data.get('deadline')
    user_id = session['user_id']

    if not all([title, target_amount, deadline]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_goal = Goal(
            user_id=user_id,
            title=title,
            target_amount=target_amount,
            deadline=deadline,
            current_amount=0.00
        )
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"message": "Goal added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to get the user's current balance
@goals_bp.route('/balance', methods=['GET'])
def get_balance():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    try:
        total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.00
        total_expense = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.00
        balance = total_income - total_expense
        return jsonify({"balance": float(balance)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to delete a goal
@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        goal = Goal.query.get(goal_id)
        if goal:
            db.session.delete(goal)
            db.session.commit()
            return jsonify({"message": "Goal deleted successfully."}), 200
        else:
            return jsonify({"error": "Goal not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
