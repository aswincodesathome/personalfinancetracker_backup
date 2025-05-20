from flask import Blueprint, request, jsonify, render_template

chatbot_bp = Blueprint('chatbot', __name__)

# ✅ Route to render the chatbot UI page (GET)
@chatbot_bp.route('/chatbot', methods=['GET'])
def chatbot_page():
    return render_template('chatbot.html')

# ✅ Route to handle chat message via JavaScript fetch (POST)
@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot_reply():
    data = request.get_json()
    message = data.get('message', '').lower()

    if "add" in message and "expense" in message:
        reply = "You can add a new expense from the 'Add Expense' section in the dashboard."
    elif "view" in message and "expenses" in message:
        reply = "To view your expenses, check the Summary or Analytics page."
    elif "income" in message:
        reply = "Your income details are available on your Dashboard."
    elif "goals" in message:
        reply = "Go to 'My Goals' to set or track your financial goals."
    elif "balance" in message:
        reply = "Your balance is calculated on the Dashboard using your total income and expenses."
    elif "hello" in message or "hi" in message:
        reply = "Hey there! 👋 I'm FinBot. How can I help you manage your money today?"
    elif "help" in message:
        reply = "I can assist with income, expenses, goals, balance, and where to find things!"
    else:
        reply = "Sorry, I didn’t understand that. Try asking about income, expenses, goals, or balance."

    return jsonify({'reply': reply})
