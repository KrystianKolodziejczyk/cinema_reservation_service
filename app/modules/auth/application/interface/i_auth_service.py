from abc import ABC, abstractmethod

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.dto.login_dto import LoginDTO


class IAuthService(ABC):
    @abstractmethod
    async def register_user(self, dto: RegisterUserDTO) -> dict[str, str]: ...

    @abstractmethod
    async def login(self, dto: LoginDTO) -> dict[str, str]: ...

    @abstractmethod
    async def logout(self, user_id: int) -> None: ...

    @abstractmethod
    async def refresh(self, token: str) -> dict[str, str]: ...
