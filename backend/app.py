from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.database import init_db, mongo
from dotenv import load_dotenv, find_dotenv
from bson.objectid import ObjectId
import bcrypt
import os
import random
import string

load_dotenv(find_dotenv(raise_error_if_not_found=True))

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

init_db(app)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to ClickSmart Backend API!"})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "xp": 0,
        "level": 1,
        "is_guest": False,
        "answered_questions": []
    }
    mongo.db.users.insert_one(new_user)
    return jsonify({"message": "User registered successfully", "username": username}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({
            "message": "Login successful",
            "username": username,
            "xp": user.get('xp', 0),
            "level": user.get('level', 1)
        }), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


@app.route('/guest_login', methods=['POST'])
def guest_login():
    request.get_json(silent=True)  # Accept empty body safely

    def generate_guest_username():
        while True:
            guest_username = "guest_" + ''.join(random.choices(string.digits, k=6))
            if not mongo.db.users.find_one({"username": guest_username}):
                return guest_username

    guest_username = generate_guest_username()

    guest_user = {
        "username": guest_username,
        "password": "",  # Empty password for guest
        "xp": 0,
        "level": 1,
        "is_guest": True,
        "answered_questions": []
    }

    mongo.db.users.insert_one(guest_user)

    return jsonify({
        "message": "Guest login successful",
        "username": guest_username,
        "xp": 0,
        "level": 1
    }), 200


@app.route('/questions', methods=['GET'])
def get_questions():
    username = request.args.get('username')
    questions = []

    if username:
        user = mongo.db.users.find_one({"username": username})
        seen_ids = user.get("answered_questions", []) if user else []
        cursor = mongo.db.questions.find({"_id": {"$nin": [ObjectId(qid) for qid in seen_ids]}})
    else:
        cursor = mongo.db.questions.find()

    for q in cursor:
        q['_id'] = str(q['_id'])
        questions.append(q)

    return jsonify(questions), 200


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')
    username = data.get('username')

    if not question_id or not selected_answer or not username:
        return jsonify({"error": "Missing data"}), 400

    question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    if not question:
        return jsonify({"error": "Question not found"}), 404

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if question_id in user.get("answered_questions", []):
        return jsonify({"error": "Question already answered"}), 400

    is_correct = (selected_answer == question['correct_answer'])
    xp_awarded = 0

    if is_correct:
        xp_awarded = question.get('xp_value', 0)
        mongo.db.users.update_one(
            {"username": username},
            {
                "$inc": {"xp": xp_awarded},
                "$push": {"answered_questions": question_id}
            }
        )

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": question['correct_answer'],
        "xp_awarded": xp_awarded
    }), 200


@app.route('/profile/<username>', methods=['GET'])
def get_user_profile(username):
    user = mongo.db.users.find_one({"username": username}, {"password": 0})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    users = mongo.db.users.find({"is_guest": {"$ne": True}}).sort("xp", -1).limit(10)
    leaderboard = []
    for user in users:
        leaderboard.append({
            "username": user["username"],
            "xp": user.get("xp", 0),
            "level": user.get("level", 1)
        })
    return jsonify(leaderboard), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
