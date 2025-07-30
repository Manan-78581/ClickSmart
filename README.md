---
<p align="center">
  <img src="https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-f7df1e?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/Authentication-Secure%20Login-blueviolet?style=for-the-badge"/>
</p>

--- 

# ClickSmart 🧠✨

**ClickSmart** is a full-stack web-based cybersecurity quiz platform built to help students practice challenging questions in an interactive and gamified environment. The app features real-time XP tracking, question difficulty levels, user authentication (with Guest Mode), and a professional UI with engaging animations.
---
## 🎯 Features

- 🧠 100 curated cybersecurity questions (Easy, Medium, Hard)
- 🔐 Login, Sign-Up, and Guest login options
- 🧩 Real-time feedback with XP rewards
- ⏭️ Skip question and End Quiz functionality
- 📈 Profile page with XP and level tracking
- 💻 Responsive and animated user interface (Bootstrap + Custom CSS)
- 🗃️ MongoDB-powered question/answer storage and analytics

---

## 🛠️ Tech Stack

| Layer       | Technology               |
|-------------|---------------------------|
| Frontend    | HTML, CSS, JavaScript, Bootstrap |
| Backend     | Flask (Python)            |
| Database    | MongoDB (with Flask-PyMongo) |
| Auth & Crypto | bcrypt for password hashing  |

---

## ⚙️ Installation & Setup

```bash
# Clone the repo
git clone https://github.com/Manan-78581/ClickSmart
cd ClickSmart

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Setup MongoDB URI in `.env`
touch .env
echo "MONGO_URI=mongodb://localhost:27017/clicksmart" >> .env

# Run Flask Server
python app.py
```
---
## 🗃️ Data Flow Diagram

```mermaid
flowchart LR
    U[User - Student]
    F[Frontend - HTML/CSS/JS]
    B[Backend - Flask]
    DB[(MongoDB)]

    U -->|Login/Answer| F
    F -->|API Requests| B
    B -->|Data Fetch/Write| DB
    DB -->|Question/XP/User| B
    B -->|Feedback/Data| F
    F -->|Show Quiz & XP| U
```
--- 

## 🧩 System Architecture
Frontend (Bootstrap + Vanilla JS)

REST APIs via Flask

MongoDB for persistent user/question storage

Environment secured via python-dotenv

```mermaid
flowchart LR
    User["🧑‍💻 User"]
    FE["🖥️ Frontend (HTML/CSS/JS)"]
    BE["⚙️ Flask Backend (Python)"]
    DB[(🗄️ MongoDB Database)]

    User <--> FE
    FE <--> BE
    BE <--> DB
```


---
## 📸 Screenshots

<img width="1919" height="861" alt="image" src="https://github.com/user-attachments/assets/848e882f-e949-48cd-905a-dea8029fcb47" />

---
## 📄 License
This project is open-source and licensed under the MIT License.

---
## ✨ Acknowledgements
Project ideation, development, and architecture by Manan Kathuria.

---
## 🙋‍♂️ Author
Made with 🖤 by Manan Kathuria

