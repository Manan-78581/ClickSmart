# ClickSmart/backend/routes/leaderboard.py
from flask import Blueprint, jsonify
from backend.database import mongo

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    users_collection = mongo.db.users

    # Find top users by XP, sort descending, limit to top 10
    leaderboard_data = list(users_collection.find(
        {},
        {"_id": 0, "username": 1, "xp": 1} # Only return username and xp
    ).sort("xp", -1).limit(10)) # -1 for descending order

    return jsonify({"leaderboard": leaderboard_data}), 200