from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities import Hall
from app.modules.cinema.domain.entities.seat import Seat
from app.modules.cinema.infrastructure.interface import IHallRepository
from app.modules.cinema.infrastructure.mappers import HallMapper
from app.modules.cinema.infrastructure.mappers.seat_mapper import SeatMapper
from app.modules.cinema.infrastructure.orm.hall_orm import HallORM


class HallRepository(IHallRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_hall(self, hall: Hall) -> int:
        hall_orm = HallMapper.to_orm(hall)

        self._session.add(hall_orm)
        await self._session.flush()

        return hall_orm.hall_id

    async def fill_hall(self, seats: list[Seat]) -> None:
        seats_orm = [SeatMapper.to_orm(seat) for seat in seats]

        self._session.add_all(seats_orm)
        await self._session.flush()

    async def delete_hall(self, hall_id: int) -> bool:
        stmt = (
            delete(HallORM)
            .where(HallORM.hall_id == hall_id)
            .returning(HallORM.hall_id)
        )

        return bool(await self._session.scalar(stmt))
