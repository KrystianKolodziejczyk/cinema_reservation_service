from abc import ABC, abstractmethod

from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.domain.entities.user import User


class IAuthRepository(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> int: ...

    @abstractmethod
    async def save_refresh_token(self, refresh_token: RefreshToken) -> None: ...

    @abstractmethod
    async def fetch_user(self, email: str) -> User: ...

    @abstractmethod
    async def delete_refresh_token(
        self, user_id: int, refresh_token_id: int
    ) -> None: ...

    @abstractmethod
    async def fetch_refresh_token(
        self, user_id: int, token: str
    ) -> RefreshToken | None: ...
