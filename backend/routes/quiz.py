# ClickSmart/backend/routes/quiz.py
from flask import Blueprint, request, jsonify, session
from backend.database import mongo
from backend.utils.question_selector import get_questions_for_user
import random

quiz_bp = Blueprint('quiz', __name__)

# In a real application, you'd protect these routes with a login_required decorator
# For now, we'll assume a user is logged in based on their username (from request data for simplicity)
# or you would use Flask's session object (session.get('username'))

@quiz_bp.route('/start', methods=['POST'])
def start_quiz():
    data = request.get_json()
    username = data.get('username') # For development, assuming username is sent
    # In production, get user from session/JWT:
    # username = session.get('username')
    
    if not username:
        return jsonify({"error": "Authentication required"}), 401

    users_collection = mongo.db.users
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_xp = user.get('xp', 0)
    questions = get_questions_for_user(user_xp, num_questions=5) # Get 5 questions per round

    # Store current quiz session questions (optional but good for tracking)
    # This might be stored in the session or a temporary collection
    # For now, we just return them.

    return jsonify({"questions": questions}), 200

@quiz_bp.route('/answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    username = data.get('username') # For development
    question_text = data.get('question_text')
    user_answer = data.get('user_answer')

    if not username or not question_text or not user_answer:
        return jsonify({"error": "Missing required data"}), 400

    users_collection = mongo.db.users
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    questions_collection = mongo.db.questions
    question = questions_collection.find_one({"text": question_text}) # Find question by text (or unique ID)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    is_correct = (user_answer == question['correct_answer'])
    xp_gained = 0
    feedback_message = ""

    if is_correct:
        xp_value = question.get('xp_value', 10) # Default XP for a question
        xp_gained = xp_value
        feedback_message = "Correct! You gained {} XP.".format(xp_gained)
        
        # Update user's XP
        new_xp = user['xp'] + xp_gained
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"xp": new_xp}}
        )
    else:
        feedback_message = "Incorrect. The correct answer was: {}".format(question['correct_answer'])

    return jsonify({
        "is_correct": is_correct,
        "xp_gained": xp_gained,
        "new_total_xp": user['xp'] + xp_gained if is_correct else user['xp'], # Return updated XP
        "feedback": feedback_message,
        "correct_answer": question['correct_answer']
    }), 200