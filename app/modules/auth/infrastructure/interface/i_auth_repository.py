from abc import ABC, abstractmethod


class IAuthRepository(ABC):
    @abstractmethod
    async def register_user(self, user) -> None: ...
