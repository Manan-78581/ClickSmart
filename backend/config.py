import os
from dotenv import load_dotenv, find_dotenv # <--- THIS LINE IS CRUCIAL: ADDED find_dotenv

# Load environment variables from .env file
# Explicitly tell load_dotenv to find the .env file by searching upwards from the script's location.
# raise_error_if_not_found=True will give an error if .env isn't found, which is good for debugging.
load_dotenv(find_dotenv(raise_error_if_not_found=True)) # <--- THIS LINE IS CRUCIAL

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key') # Provide a default for local testing
    MONGO_URI = os.getenv('MONGO_URI') # This should come from .env

    # DEBUGGING PRINTS REMOVED FROM HERE