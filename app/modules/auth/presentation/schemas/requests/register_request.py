from pydantic import BaseModel, Field


class RegisterUserRequest(BaseModel):
    email: str = Field(min_length=5)
    password: str = Field(min_length=6)
    password_repeat: str
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
