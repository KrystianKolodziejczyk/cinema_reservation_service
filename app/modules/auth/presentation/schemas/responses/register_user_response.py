from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    access_token: str
    refresh_token: str
