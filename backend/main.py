from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import json
import hashlib
import secrets


# ==========================================
# Create FastAPI application
# ==========================================

app = FastAPI()


# ==========================================
# Enable CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# MongoDB Connection
# ==========================================

client = MongoClient("mongodb://localhost:27017/")

database = client["quiz_database"]

results_collection = database["test_results"]

users_collection = database["users"]


# ==========================================
# Load MCQ Dataset
# ==========================================

with open(
    "dataset/cs_questions.json",
    "r",
    encoding="utf-8"
) as file:

    questions = json.load(file)


# ==========================================
# Request Model - Register
# ==========================================

class RegisterRequest(BaseModel):

    student_name: str
    password: str
    confirm_password: str


# ==========================================
# Request Model - Login
# ==========================================

class LoginRequest(BaseModel):

    student_name: str
    password: str


# ==========================================
# Request Model - Check Answer
# ==========================================

class AnswerRequest(BaseModel):

    question_index: int
    answer_index: int


# ==========================================
# Request Model - Save Result
# ==========================================

class ResultRequest(BaseModel):

    student_name: str
    score: int
    total_questions: int
    result: str


# ==========================================
# Password Hash Function
# ==========================================

def hash_password(password: str, salt: str):

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()


# ==========================================
# Home API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AI Academic Assistant is running"
    }


# ==========================================
# Register User
# ==========================================

@app.post("/register")
def register_user(data: RegisterRequest):

    # Check empty name
    if not data.student_name.strip():

        return {
            "success": False,
            "message": "Username is required."
        }


    # Check empty password
    if not data.password:

        return {
            "success": False,
            "message": "Password is required."
        }


    # Check password confirmation
    if data.password != data.confirm_password:

        return {
            "success": False,
            "message": "Passwords do not match."
        }


    # Check if user already exists
    existing_user = users_collection.find_one({
        "student_name": data.student_name
    })

    if existing_user:

        return {
            "success": False,
            "message": "Username already exists."
        }


    # Create secure salt
    salt = secrets.token_hex(16)


    # Hash password
    password_hash = hash_password(
        data.password,
        salt
    )


    # Create user document
    user_document = {

        "student_name": data.student_name,

        "password_hash": password_hash,

        "salt": salt,

        "created_at": datetime.now().isoformat()
    }


    # Save user in MongoDB
    users_collection.insert_one(
        user_document
    )


    return {

        "success": True,

        "message": "Registration successful!"
    }


# ==========================================
# Login User
# ==========================================

@app.post("/login")
def login_user(data: LoginRequest):

    user = users_collection.find_one({
        "student_name": data.student_name
    })

    if not user:

        return {
            "success": False,
            "message": "Username or password is incorrect."
        }


    password_hash = hash_password(
        data.password,
        user["salt"]
    )


    if password_hash != user["password_hash"]:

        return {
            "success": False,
            "message": "Username or password is incorrect."
        }


    return {

        "success": True,

        "message": "Login successful!",

        "student_name": user["student_name"]
    }


# ==========================================
# Get Questions
# ==========================================

@app.get("/questions")
def get_questions():

    result = []

    for item in questions:

        result.append({
            "question": item["question"],
            "options": item["options"]
        })

    return result


# ==========================================
# Check Answer
# ==========================================

@app.post("/check-answer")
def check_answer(data: AnswerRequest):

    question = questions[data.question_index]

    correct_index = question["answer_index"]

    option_letters = ["A", "B", "C", "D"]

    correct_letter = option_letters[correct_index]

    if data.answer_index == correct_index:

        return {
            "correct": True,
            "correct_answer": correct_letter,
            "message": "Correct Answer!"
        }

    return {
        "correct": False,
        "correct_answer": correct_letter,
        "message": "Wrong Answer!"
    }


# ==========================================
# Save Test Result to MongoDB
# ==========================================

@app.post("/save-result")
def save_result(data: ResultRequest):

    result_document = {

        "student_name": data.student_name,

        "score": data.score,

        "total_questions": data.total_questions,

        "result": data.result,

        "date_time": datetime.now().isoformat()
    }

    results_collection.insert_one(
        result_document
    )

    return {
        "message": "Test result saved successfully!"
    }
# ==========================================
# Get Test History
# ==========================================

@app.get("/history/{student_name}")
def get_history(student_name: str):

    history = []

    results = results_collection.find(
        {
            "student_name": student_name
        },
        {
            "_id": 0
        }
    ).sort(
        "date_time",
        -1
    )

    for item in results:

        history.append({
            "student_name": item.get(
                "student_name",
                ""
            ),

            "score": item.get(
                "score",
                0
            ),

            "total_questions": item.get(
                "total_questions",
                10
            ),

            "result": item.get(
                "result",
                ""
            ),

            "date_time": item.get(
                "date_time",
                ""
            )
        })

    return history