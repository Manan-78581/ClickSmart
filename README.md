# Click Smart - Security Awareness Quiz Game

Welcome to Click Smart, an interactive quiz game designed to enhance your cybersecurity awareness!

## Project Overview

Click Smart aims to educate users on common cybersecurity best practices through an engaging quiz format. The game features an XP system, where question difficulty adapts based on a user's accumulated experience points.

## Features

* **User Authentication:** Secure sign-up and login.
* **Adaptive Quiz:** Questions dynamically adjust based on your XP level.
* **XP System:** Earn points for correct answers.
* **Leaderboard:** Compete with other users.
* **Learning Feedback:** (To be implemented) Get explanations for incorrect answers.

## Tech Stack

* **Frontend:** HTML, CSS, JavaScript (Vanilla JS)
* **Backend:** Python (Flask)
* **Database:** SQLite (for development), PostgreSQL/MySQL (for production)

## Setup and Installation

### Prerequisites

* Python 3.x
* Node.js & npm/yarn (for frontend dev dependencies like `live-server`)

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the virtual environment:**
    * On macOS/Linux/Git Bash: ```bash source venv/bin/activate ```
    * On Windows (CMD): ```cmd venv\Scripts\activate ```
    * On Windows (PowerShell): ```powershell .\venv\Scripts\Activate.ps1 ```
4.  **Install backend dependencies:**
    ```bash
    pip install -r ../requirements.txt
    ```
5.  **Initialize the database (run this once):**
    You'll need to add code to `app.py` or `database.py` to create tables based on `models.py`. A typical setup involves something like:
    ```python
    # In app.py or a setup script
    from app import app, db
    with app.app_context():
        db.create_all()
    ```
6.  **Run the Flask application:**
    ```bash
    flask run
    ```
    (Ensure `FLASK_APP=app.py` is set in your environment or `export FLASK_APP=app.py` on Linux/macOS/Git Bash)

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install frontend development dependencies (e.g., `live-server`):**
    ```bash
    npm install
    # Or if you prefer yarn:
    # yarn install
    ```
3.  **Start the development server:**
    ```bash
    npm start # This runs the 'start' script defined in package.json
    ```
    This will typically open `index.html` in your browser.

## Project Structure

```bash
# Run 'tree -L 4 ClickSmart' from the parent directory
# after you create the project structure.
```

## Contributing

Feel free to fork, contribute, or open issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

