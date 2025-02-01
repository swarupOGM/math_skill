from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from typing import List


class RegisterUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Treated as username
    age: int
    user_class: str
    country: str
    password: str
    confirm_password: str
    role: Optional[str] = "general"

    # Ensure password and confirm_password match
    @staticmethod
    def validate_passwords(cls, values):
        if values["password"] != values["confirm_password"]:
            raise ValueError("Passwords do not match.")
        return values


class LoginSchema(BaseModel):
    email: EmailStr  # Used as username
    password: str


class RegisterResponseSchema(BaseModel):
    message: str
    enrolled_id: int


class ResponseSchema(BaseModel):
    message: str
    enrolled_id: int
    admin: int


# Pydantic schemas for input validation
class GenerateQuestionSchema(BaseModel):
    count: int  # Total number of questions to generate
    operation_level: str  # e.g., "2D", "3D"
    points: int  # Points for each question


class QuestionSchema(BaseModel):
    id: int
    operation_type: str
    operation_level: str
    first_number: float
    second_number: float
    answer: float
    points: int

    class Config:
        orm_mode = True


# Schema for individual question in the list
class QuestionInListSchema(BaseModel):
    id: int
    operation_type: str
    operation_level: str
    first_number: float
    second_number: float
    answer: float
    points: int

    class Config:
        orm_mode = True


# Schema for the list of questions
class QuestionListResponseSchema(BaseModel):
    questions: List[QuestionInListSchema]

    class Config:
        orm_mode = True
