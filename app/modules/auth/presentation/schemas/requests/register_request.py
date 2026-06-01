from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    password_repeat: str
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
