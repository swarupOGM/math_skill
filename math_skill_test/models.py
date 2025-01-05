from sqlalchemy import Column, Integer, String
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