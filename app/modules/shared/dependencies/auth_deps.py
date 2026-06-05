import jwt
from fastapi import Request

from app.modules.shared.config.settings import settings
from app.modules.shared.exceptions.expired_token_error import ExpiredTokenError
from app.modules.shared.exceptions.invalid_token_error import InvalidTokenError


async def get_current_user(request: Request) -> dict[str, int | str]:
    try:
        token = request.headers.get("Authorization")
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return {"user_id": int(payload["sub"]), "role": payload["role"]}
    except jwt.ExpiredSignatureError as e:
        raise ExpiredTokenError(status_code=401, detail="Token expired") from e
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError(status_code=409, detail="Invalid token") from e
