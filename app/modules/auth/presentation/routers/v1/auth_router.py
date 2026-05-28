from fastapi import APIRouter

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.presentation.schemas.requests import (
    RegisterUserRequest,
)

router = APIRouter(prefix="/v1/auth")


# ===============


@router.post("/register")
async def register_user(body: RegisterUserRequest):
    dto = RegisterUserDTO(**body.model_dump())
    print(dto)
