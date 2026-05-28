from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.interface import IAuthService


class AuthService(IAuthService):
    def __init__(self, repository) -> None:
        self._repository = repository

    async def register_user(self, dto: RegisterUserDTO) -> None:
        pass
