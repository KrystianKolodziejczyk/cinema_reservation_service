from sqlalchemy import case, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_expression

from app.modules.cinema.application.dto import (
    MovieData,
    ScreeningDetailsDTO,
    SeatData,
)
from app.modules.cinema.application.excpetions import ScreeningNotFoundError
from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import IScreeningRepository
from app.modules.cinema.infrastructure.mappers import ScreeningMapper
from app.modules.cinema.infrastructure.orm import (
    HallORM,
    ReservationORM,
    ReservedSeatORM,
    ScreeningORM,
    SeatORM,
)


class ScreeningRepository(IScreeningRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_screenings(self, screenings: list[Screening]) -> None:
        screenings_orm = [ScreeningMapper.to_orm(screening) for screening in screenings]

        self._session.add_all(screenings_orm)
        await self._session.flush()

    async def delete_screening(self, screening_id: int) -> bool:
        stmt = (
            delete(ScreeningORM)
            .where(ScreeningORM.screening_id == screening_id)
            .returning(ScreeningORM.screening_id)
        )

        return bool(await self._session.scalar(stmt))

    async def fetch_basic_screening(self, screening_id: int) -> Screening:
        stmt = select(ScreeningORM).where(ScreeningORM.screening_id == screening_id)
        screening_orm = await self._session.scalar(stmt)

        if screening_orm is None:
            raise ScreeningNotFoundError(
                status_code=404, detail="Screening does not exist"
            )

        return ScreeningMapper.to_entity(screening_orm=screening_orm)

    async def save_screening(self, screening: Screening) -> None:
        screening_orm = ScreeningMapper.to_orm(screening)

        await self._session.merge(screening_orm)
        await self._session.flush()

    async def fetch_screening_with_relations(
        self, screening_id: int
    ) -> ScreeningDetailsDTO:
        is_occupied = (
            select(ReservedSeatORM.seat_id)
            .join(ReservationORM)
            .where(
                ReservedSeatORM.seat_id == SeatORM.seat_id,
                ReservationORM.screening_id == screening_id,
            )
            .correlate(SeatORM)
            .exists()
        )

        stmt = (
            select(ScreeningORM)
            .where(ScreeningORM.screening_id == screening_id)
            .options(
                selectinload(ScreeningORM.movie),
                selectinload(ScreeningORM.hall)
                .selectinload(HallORM.seats)
                .options(
                    with_expression(
                        SeatORM.status,
                        case((is_occupied, "occupied"), else_="free"),
                    )
                ),
            )
        )

        screening_orm = await self._session.scalar(stmt)

        if not screening_orm:
            return None

        return ScreeningDetailsDTO(
            screening_id=screening_orm.screening_id,
            movie=MovieData(
                screening_orm.movie.title,
                description=screening_orm.movie.description,
                director=screening_orm.movie.director,
                duration=screening_orm.movie.duration,
                genre=screening_orm.movie.genre,
                rating=screening_orm.movie.rating,
            ),
            starts_at=screening_orm.starts_at,
            hall_name=screening_orm.hall.hall_name,
            seats=[
                SeatData(
                    row=seat.row,
                    number=seat.number,
                    seat_type=seat.seat_type,
                    status=seat.status,
                    price=screening_orm.price_normal
                    if seat.seat_type == "normal"
                    else screening_orm.price_vip,
                )
                for seat in screening_orm.hall.seats
            ],
        )
