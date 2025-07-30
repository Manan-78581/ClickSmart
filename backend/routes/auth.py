# ClickSmart/backend/routes/auth.py
from flask import Blueprint, request, jsonify
from backend.database import mongo
from bcrypt import hashpw, gensalt, checkpw
import datetime # For timestamps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    users_collection = mongo.db.users

    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409

    # Hash the password
    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    user_data = {
        "username": username,
        "password_hash": hashed_password,
        "xp": 0, # New users start with 0 XP
        "created_at": datetime.datetime.utcnow(),
        "last_login": datetime.datetime.utcnow()
    }
    users_collection.insert_one(user_data)

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    users_collection = mongo.db.users
    user = users_collection.find_one({"username": username})

    if user and checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        # For simplicity, we'll return user data directly.
        # In a real app, you'd likely use JWTs or Flask sessions.
        
        # Update last_login timestamp
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.datetime.utcnow()}}
        )

        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user["username"],
                "xp": user["xp"]
                # Do NOT send password_hash or _id to frontend
            }
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401