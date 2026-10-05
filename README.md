# AI-Powered Quiz Generator

An AI-powered Computer Science quiz platform developed using Python, FastAPI, FLAN-T5, HTML, CSS, JavaScript, and MongoDB.

## Project Overview

The AI-Powered Quiz Generator is an interactive Computer Science quiz application that allows users to create an account, log in securely, take randomized multiple-choice tests, view their scores, and check their previous test history.

The project uses a Computer Science question dataset containing 100 questions. Each test randomly selects 10 questions from the dataset.

## Features

- User registration and login
- Password hashing for secure password storage
- Randomized 10-question Computer Science tests
- Four multiple-choice options for each question
- Instant answer checking
- Automatic score calculation
- PASS/FAIL result
- Test history stored in MongoDB
- User-specific test history
- Start Next Test functionality
- Professional and responsive web interface
- FLAN-T5 based NLP/model training component

## Technologies Used

- Python
- FastAPI
- Uvicorn
- FLAN-T5
- Transformers
- PyTorch
- SentencePiece
- MongoDB
- PyMongo
- HTML
- CSS
- JavaScript
- JSON
- Git & GitHub
- VS Code

## Project Structure

```text
AI-Powered-Quiz-Generator/
│
├── backend/
│   └── main.py
│
├── dataset/
│   ├── cs_questions.json
│   ├── prepare_dataset.py
│   ├── check_dataset.py
│   └── clean_dataset.py
│
├── frontend/
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   ├── quiz.html
│   ├── script.js
│   └── style.css
│
├── model/
│   └── train_model.py
│
├── requirements.txt
├── .gitignore
└── README.md

Application Flow

User Registration
        ↓
      Login
        ↓
    Home Page
        ↓
     Start Test
        ↓
Random 10 Questions
        ↓
   Select Answer
        ↓
   Check Answer
        ↓
   Score Calculation
        ↓
     PASS / FAIL
        ↓
 Save Result to MongoDB
        ↓
   Test History
        ↓
   Start Next Test

Dataset

The project uses a Computer Science question dataset containing 100 questions.

Each question contains:

Question

Four multiple-choice options

Correct answer index


The dataset preparation process converts questions into a consistent four-option format and creates training data for the FLAN-T5 model.

MongoDB

MongoDB is used to store:

Registered user information

Test results

Student name

Score

Total questions

PASS/FAIL result

Date and time


The database used by the application is:

quiz_database

The main collections are:

users
test_results

Password Security

User passwords are not stored as plain text.

The application uses:

PBKDF2

SHA-256

Random salt


This converts the password into a secure hash before storing it in MongoDB.

Backend Setup

1. Install Python

Python 3.12 is recommended for this project.

2. Install Dependencies

Open the terminal in the project folder and run:

pip install -r requirements.txt

3. Start FastAPI Backend

Run:

py -3.12 -m uvicorn backend.main:app --reload

The backend will run at:

http://127.0.0.1:8000

Frontend Setup

Open the frontend folder in VS Code.

Open:

login.html

using the VS Code Live Server extension.

The application can then be used through the browser.

MongoDB Setup

Make sure MongoDB is running locally.

The application connects to:

mongodb://localhost:27017/

The application automatically creates/uses:

quiz_database

with the required collections.

API Endpoints

The FastAPI backend provides endpoints for:

POST /register
POST /login
GET  /questions
POST /check-answer
POST /save-result
GET  /history/{student_name}

Model Component

The project includes a FLAN-T5 based model training component for text-to-text language-model functionality.

The model training files and large trained model files are kept locally and are excluded from the GitHub repository using .gitignore.

Important Note

Large model files and training checkpoints are not included in this repository because of their file size.

The repository contains the source code, dataset preparation files, frontend, backend, configuration files, and project documentation required to understand and run the application.

Future Enhancements

AI-generated quiz questions

Difficulty-based quizzes

More Computer Science topics

Performance analytics

Timer-based tests

Improved question generation

Deployment as a web application


Author

Aswani Mandapaka

BTech CSE (AI & Data Science) Graduate