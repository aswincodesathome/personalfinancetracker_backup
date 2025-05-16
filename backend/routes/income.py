from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from models.income import Income
from db import db

income_bp = Blueprint('income', __name__)

# ✅ Show Add Income Form
@income_bp.route('/add_income/<int:user_id>', methods=['GET'])
def show_add_income(user_id):
    return render_template('add_income.html', user_id=user_id)

# ✅ Handle Income Form Submission (using SQLAlchemy)
@income_bp.route('/income/<int:user_id>', methods=['POST'])
def add_income(user_id):
    source = request.form.get('category')
    amount = request.form.get('amount')
    received_on_raw = request.form.get('date')
    from datetime import datetime
    received_on = datetime.strptime(received_on_raw, '%Y-%m-%d').date()

    new_income = Income(
        amount=float(amount),
        source=source,
        received_on=received_on,  # ✅ FIXED
        user_id=user_id
    )


    try:
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('users.dashboard'))  # Change this if dashboard route is different
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}", 500

# ✅ API: Get incomes for a user (optional API route)
@income_bp.route('/income/<int:user_id>', methods=['GET'])
def get_incomes(user_id):
    try:
        incomes = Income.query.filter_by(user_id=user_id).order_by(Income.date.desc()).all()
        income_list = [{
            'id': i.id,
            'source': i.source,
            'amount': i.amount,
            'date': i.date
        } for i in incomes]

        return jsonify(income_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
