import jwt
from fastapi import Request

from app.modules.shared.config.settings import settings


async def get_current_user(request: Request) -> int:
    try:
        token = request.headers.get("Authorization")
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return int(payload["sub"])
    except jwt.ExpiredSignatureError as e:
        raise ValueError("EXPIRED") from e  # TODO: zmień
    except jwt.InvalidTokenError as e:
        raise ValueError("WRONGGGGGGGGGGGGGGGG TOKENENNNNNN") from e
