from pydantic import BaseModel, EmailStr, Field


class RegisterUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Treated as username
    age: int
    user_class: str
    country: str
    password: str
    confirm_password: str

    # Ensure password and confirm_password match
    @staticmethod
    def validate_passwords(cls, values):
        if values["password"] != values["confirm_password"]:
            raise ValueError("Passwords do not match.")
        return values


class LoginSchema(BaseModel):
    email: EmailStr  # Used as username
    password: str


class ResponseSchema(BaseModel):
    message: str
    enrolled_id: int