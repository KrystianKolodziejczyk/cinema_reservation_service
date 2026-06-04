from abc import abstractmethod

from app.modules.cinema.domain.entities import Hall


class IHallRepository:
    @abstractmethod
    async def create_hall(self, hall: Hall) -> None: ...
