from flask import Blueprint, request, jsonify
from config import get_db_connection
import mysql.connector

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['POST'])  # POST /categories/
def add_category():
    data = request.get_json()
    name = data.get('name')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO category (name) VALUES (%s)", (name,))
        conn.commit()
        return jsonify({"message": "Category added successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@categories_bp.route('/', methods=['GET'])  # GET /categories/
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@categories_bp.route('/<int:category_id>', methods=['DELETE'])  # DELETE /categories/5
def delete_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        conn.commit()
        return jsonify({"message": "Category deleted successfully!"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
