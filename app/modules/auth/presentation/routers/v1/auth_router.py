from fastapi import APIRouter

router = APIRouter(prefix="/v1/auth")


# ===============


@router.post("/register")
async def register_user():
    return {"message": "working"}
