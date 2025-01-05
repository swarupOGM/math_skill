from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User
from schemas import RegisterUserSchema, LoginSchema, ResponseSchema
from utils import hash_password, verify_password
from secrets import compare_digest

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=ResponseSchema)
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

    return {"message": "Login successful.", "enrolled_id": user.id}