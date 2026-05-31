from abc import ABC, abstractmethod

from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.domain.entities.user import User


class IAuthRepository(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> int: ...

    @abstractmethod
    async def save_refresh_token(self, refresh_token: RefreshToken) -> None: ...

    @abstractmethod
    async def fetch_password(self, email: str) -> User: ...

    @abstractmethod
    async def revoke_refresh_token(self, user_id: int) -> None: ...
