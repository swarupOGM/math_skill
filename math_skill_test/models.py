from sqlalchemy import Column, Integer, String, Float, Enum
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # Used as username
    age = Column(Integer, nullable=False)
    user_class = Column(String, nullable=False)
    country = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum("admin", "general", name="user_roles"), nullable=True, default="general")

# Define database models


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String, nullable=False)  # Addition, Subtraction, etc.
    operation_level = Column(String, nullable=False)  # 2D, 3D, etc.
    first_number = Column(Float, nullable=False)
    second_number = Column(Float, nullable=False)
    answer = Column(Float, nullable=False)
    points = Column(Integer, nullable=False)  # Points assigned for each question