from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from config import get_db_connection
import mysql.connector

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/add_expense/<int:user_id>', methods=['GET'])
def add_expense_page(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Load category options
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()

        # Load payment method options (from updated table)
        cursor.execute("SELECT payment_method_id, method_name FROM payment_method")
        payment_methods = cursor.fetchall()

        return render_template('add_expense.html', user_id=user_id, categories=categories, payment_methods=payment_methods)

    except mysql.connector.Error as err:
        flash(f"Error loading form options: {err}", "error")
        return render_template('add_expense.html', user_id=user_id, categories=[], payment_methods=[])

    finally:
        cursor.close()
        conn.close()
@expenses_bp.route('/expense/<int:user_id>', methods=['POST'])
def add_expense(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    spent_on = request.form.get('spent_on')
    category_name = request.form.get('category_name')
    description = request.form.get('description')
    amount = request.form.get('amount')
    payment_method_name = request.form.get('payment_method_name')

    try:
        # ✅ Ensure no unread results remain
        cursor.reset()

        # ✅ Get category_id
        cursor.execute("SELECT category_id FROM category WHERE name = %s", (category_name,))
        category = cursor.fetchone()
        if not category:
            flash("Invalid category name.", "error")
            return redirect(url_for('expenses.add_expense_page', user_id=user_id))
        category_id = category['category_id']

        cursor.reset()

        # ✅ Get payment_method_id (without user_id filter)
        cursor.execute("SELECT payment_method_id FROM payment_method WHERE method_name = %s", (payment_method_name,))
        method = cursor.fetchone()
        if not method:
            flash("Invalid payment method.", "error")
            return redirect(url_for('expenses.add_expense_page', user_id=user_id))
        payment_method_id = method['payment_method_id']



        cursor.reset()

        # ✅ Insert expense
        cursor.execute("""
            INSERT INTO expenses (user_id, spent_on, category_id, description, amount, payment_method_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, spent_on, category_id, description, amount, payment_method_id))

        conn.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('users.dashboard', user_id=user_id))

    except mysql.connector.Error as err:
        flash(f"Error adding expense: {err}", "error")
        return redirect(url_for('expenses.add_expense_page', user_id=user_id))

    finally:
        cursor.close()
        conn.close()

