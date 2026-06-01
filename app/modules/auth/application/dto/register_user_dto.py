from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserDTO:
    email: str
    password: str
    password_repeat: str
    first_name: str
    last_name: str
