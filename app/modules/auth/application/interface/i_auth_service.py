from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    async def register_user(self, dto) -> None: ...
