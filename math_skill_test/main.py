from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User, Question
from schemas import (RegisterUserSchema, LoginSchema, ResponseSchema, GenerateQuestionSchema, QuestionSchema,
                     RegisterResponseSchema, QuestionListResponseSchema)
from utils import hash_password, verify_password
from secrets import compare_digest
import random
from typing import List

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=RegisterResponseSchema)
def register_user(user: RegisterUserSchema, db: Session = Depends(get_db)):
    # Check if email (used as username) already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    # Check if password and confirm_password match
        # Validate password and confirm password
    if not compare_digest(user.confirm_password, user.password):
        raise HTTPException(status_code=400, detail="Password and confirm password do not match.")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create a new user
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,  # Using email as username
        age=user.age,
        user_class=user.user_class,
        country=user.country,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully.", "enrolled_id": new_user.id}


@app.post("/login", response_model=ResponseSchema)
def login_user(credentials: LoginSchema, db: Session = Depends(get_db)):
    # Find the user by email (acting as username)
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return {"message": "Login successful.", "enrolled_id": user.id, "admin": 1 if user.role == "admin" else 0}


def generate_numbers(operation_level: str) -> tuple[float, float]:
    """
    Generates two numbers based on the operation level.

    :param operation_level: Difficulty level of the operation ('1D', '2D', etc.).
    :return: A tuple containing two numbers.
    """
    if operation_level == "1D":  # Single-digit numbers
        first_number = random.randint(1, 9)
        second_number = random.randint(1, 9)
    elif operation_level == "2D":  # Two-digit numbers
        first_number = random.randint(10, 99)
        second_number = random.randint(10, 99)
    elif operation_level == "3D":  # Three-digit numbers
        first_number = random.randint(100, 999)
        second_number = random.randint(100, 999)
    else:
        raise ValueError("Invalid operation level. Choose '1D', '2D', or '3D'.")

    return first_number, second_number


def calculate_answer(first_number: float, second_number: float, operation_type: str) -> float:
    """
    Calculates the answer based on the operation type.

    :param first_number: The first operand.
    :param second_number: The second operand.
    :param operation_type: The type of mathematical operation ('Addition', 'Subtraction', etc.).
    :return: The calculated answer.
    """
    if operation_type == "Addition":
        return first_number + second_number
    elif operation_type == "Subtraction":
        return first_number - second_number
    elif operation_type == "Multiplication":
        return first_number * second_number
    elif operation_type == "Division":
        # Handle division to avoid zero division errors
        return round(first_number / second_number, 2) if second_number != 0 else 0
    else:
        raise ValueError("Invalid operation type. Choose 'Addition', 'Subtraction', 'Multiplication', or 'Division'.")


@app.post("/generate-questions", response_model=List[QuestionSchema])
def generate_questions(payload: GenerateQuestionSchema, db: Session = Depends(get_db)):
    # # Delete existing questions
    # db.query(Question).delete()
    # db.commit()

    # Initialize variables
    questions = []
    count_per_operation = payload.count // 4
    operations = ["Addition", "Subtraction", "Multiplication", "Division"]

    # Generate questions
    for operation_type in operations:
        for _ in range(count_per_operation):
            first_number, second_number = generate_numbers(payload.operation_level)
            answer = calculate_answer(first_number, second_number, operation_type)

            # Create and save question
            question = Question(
                operation_type=operation_type,
                operation_level=payload.operation_level,
                first_number=first_number,
                second_number=second_number,
                answer=answer,
                points=payload.points
            )
            db.add(question)
            db.commit()  # Commit to generate `id`
            db.refresh(question)
            questions.append(question)  # Append ORM model instance to the list

    return questions


@app.get("/question/list", response_model=QuestionListResponseSchema)
def list_questions(db: Session = Depends(get_db)):
    # Query all questions from the database
    questions = db.query(Question).all()

    # Format the questions as per the requested structure
    formatted_questions = {
        "questions": [
            {
                "id": question.id,
                "operation_type": question.operation_type,
                "operation_level": question.operation_level,
                "first_number": question.first_number,
                "second_number": question.second_number,
                "answer": question.answer,
                "points": question.points
            }
            for question in questions
        ]
    }

    return formatted_questions

