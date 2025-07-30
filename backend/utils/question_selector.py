# ClickSmart/backend/utils/question_selector.py
import random
from backend.database import mongo

def get_questions_for_user(user_xp, num_questions=5):
    """
    Selects a set of questions for the user based on their XP level.
    The logic aims to provide a mix of difficulties as XP increases.
    """
    questions_collection = mongo.db.questions
    pipeline = []

    # Define XP ranges for difficulty focus
    if user_xp < 50:
        # Mostly easy questions for beginners
        difficulty_mix = {'easy': 0.8, 'medium': 0.2, 'hard': 0.0}
    elif 50 <= user_xp < 200:
        # Mix of easy and medium, some hard
        difficulty_mix = {'easy': 0.3, 'medium': 0.5, 'hard': 0.2}
    else:
        # More medium and hard questions
        difficulty_mix = {'easy': 0.1, 'medium': 0.4, 'hard': 0.5}

    selected_questions = []
    
    # Attempt to fetch questions based on the mix
    for difficulty, proportion in difficulty_mix.items():
        if proportion > 0:
            count_to_fetch = int(num_questions * proportion)
            # Find questions of this difficulty, exclude _id for client-side
            # and limit to slightly more than needed, then shuffle
            
            # Use aggregation pipeline for more flexibility and potential future features
            # (e.g., excluding already answered questions for this user)
            
            # Simple find for now:
            candidate_questions = list(questions_collection.find(
                {"difficulty": difficulty},
                {"_id": 0} # Exclude MongoDB's default _id field
            ))
            random.shuffle(candidate_questions)
            selected_questions.extend(candidate_questions[:count_to_fetch])

    # If we don't have enough questions due to uneven distribution or small pool,
    # or if we have too many, adjust.
    random.shuffle(selected_questions)
    
    # Ensure exactly num_questions are returned.
    # If not enough, fill with random easy questions (fallback).
    if len(selected_questions) < num_questions:
        remaining_needed = num_questions - len(selected_questions)
        fallback_questions = list(questions_collection.find(
            {}, {"_id": 0} # Get any questions
        ))
        random.shuffle(fallback_questions)
        selected_questions.extend(fallback_questions[:remaining_needed])
    
    return selected_questions[:num_questions]