import json
import os # Import the os module for path manipulation
from flask import Flask
from backend.config import Config
from backend.database import init_db, mongo

# Initialize a Flask app context for database operations
# This is necessary because Flask-PyMongo needs an app context
# to access configuration and the MongoDB connection.
app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

def load_questions():
    """
    Loads questions from questions.json into the MongoDB database.
    It checks if the collection is empty before loading to prevent duplicates
    on accidental re-runs.
    """
    with app.app_context(): # Ensure we are within the Flask application context
        questions_collection = mongo.db.questions
        
        print("Checking if questions collection is empty...")
        # count_documents({}) is an efficient way to check if a collection has any documents
        if questions_collection.count_documents({}) > 0:
            print("Questions already exist in the database. Skipping load.")
            # If you ever need to clear and reload, uncomment the lines below:
            # print("Clearing existing questions...")
            # questions_collection.delete_many({})
            # print("Existing questions cleared. Proceeding to load new questions.")
        else:
            print("Questions collection is empty. Loading questions from data/questions.json...")
            
            # Construct the absolute path to the questions.json file.
            # os.path.dirname(__file__) gets the directory of the current script (load_data.py).
            # os.path.join safely concatenates path components, handling OS differences.
            json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'questions.json')
            
            try:
                # *** THIS IS THE CRUCIAL FIX: Changed from 'utf-8' to 'utf-8-sig' ***
                with open(json_file_path, 'r', encoding='utf-8-sig') as f: 
                    questions_data = json.load(f)
                
                questions_collection.insert_many(questions_data)
                print(f"Successfully loaded {len(questions_data)} questions into MongoDB.")
            except FileNotFoundError:
                print(f"Error: The file '{json_file_path}' was not found.")
                print("Please ensure 'questions.json' is in the 'backend/data/' directory.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from '{json_file_path}': {e}")
                print("This often means the file is empty, corrupted, or has unexpected characters (like a BOM).")
                print("Please check the 'questions.json' file for syntax errors or invisible characters.")
            except Exception as e:
                print(f"An unexpected error occurred during data loading: {e}")

if __name__ == '__main__':
    load_questions()