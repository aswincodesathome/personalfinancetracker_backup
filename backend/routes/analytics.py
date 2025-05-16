from flask import Blueprint, jsonify, render_template, session, redirect, url_for
from sqlalchemy import text
from db import db

analytics_bp = Blueprint('analytics_bp', __name__)

@analytics_bp.route('/<int:user_id>')
def show_analytics(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('users.login_get'))
    return render_template('analytics.html', user_id=user_id)

# API: Monthly Expense Summary
@analytics_bp.route('/monthly-summary/<int:user_id>')
def get_monthly_summary(user_id):
    query = text("""
        SELECT 
            MONTH(spent_on) AS month, 
            SUM(amount) AS total_spent
        FROM expenses
        WHERE user_id = :user_id
        GROUP BY month
        ORDER BY month;
    """)
    result = db.session.execute(query, {"user_id": user_id})
    data = [{"month": row[0], "total_spent": row[1]} for row in result.fetchall()]
    return jsonify(data)

# API: Top Categories
@analytics_bp.route('/top-categories/<int:user_id>')
def get_top_categories(user_id):
    query = text("""
        SELECT 
            c.name AS category, 
            SUM(e.amount) AS total_spent
        FROM expenses e
        JOIN category c ON e.category_id = c.category_id
        WHERE e.user_id = :user_id
        GROUP BY c.name
        ORDER BY total_spent DESC
        LIMIT 5;
    """)
    result = db.session.execute(query, {"user_id": user_id})
    data = [{"category": row[0], "total_spent": row[1]} for row in result.fetchall()]
    return jsonify(data)

# API: Daily Spending (Last 30 days)
@analytics_bp.route('/daily-spending/<int:user_id>')
def get_daily_spending(user_id):
    query = text("""
        SELECT 
            spent_on AS date, 
            SUM(amount) AS total_spent
        FROM expenses
        WHERE user_id = :user_id
        AND spent_on >= CURDATE() - INTERVAL 30 DAY
        GROUP BY spent_on
        ORDER BY spent_on;
    """)
    result = db.session.execute(query, {"user_id": user_id})
    data = [{"date": row[0].strftime('%Y-%m-%d'), "total_spent": row[1]} for row in result.fetchall()]
    return jsonify(data)
