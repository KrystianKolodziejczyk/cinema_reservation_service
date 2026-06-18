from dataclasses import asdict
from datetime import timedelta

from sqlalchemy.exc import IntegrityError

from app.modules.cinema.application.dto import (
    AddScreeningDTO,
    ReservationHoldDTO,
    ScreeningDetailsDTO,
    UpdateScreeningDTO,
)
from app.modules.cinema.application.excpetions import (
    HallNotFoundError,
    MovieNotFoundError,
    PermissionDeniedError,
    ScreeningNotFoundError,
    SeatUnavailableError,
)
from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.domain.entities import Screening, ScreeningSeat
from app.modules.cinema.infrastructure.interface import (
    IHallRepository,
    IMovieRepository,
    IReservationHoldRepository,
    IScreeningRepository,
    IScreeningSeatRepository,
)


class ScreeningService(IScreeningService):
    def __init__(
        self,
        screening_repository: IScreeningRepository,
        hall_repository: IHallRepository,
        redis_repository: IReservationHoldRepository,
        screening_seat_repository: IScreeningSeatRepository,
        movie_repository: IMovieRepository,
    ) -> None:
        self._screening_repository = screening_repository
        self._hall_repository = hall_repository
        self._redis_repository = redis_repository
        self._screening_seat_repository = screening_seat_repository
        self._movie_repository = movie_repository

    def _user_role_check(self, user_role: str) -> None:
        if user_role != "admin":
            raise PermissionDeniedError(status_code=403, detail="Permision denied")

    async def add_screening(self, dto: AddScreeningDTO, user_role: str) -> list[int]:
        self._user_role_check(user_role=user_role)

        try:
            movie = await self._movie_repository.fetch_movie(movie_id=dto.movie_id)
        except IntegrityError as e:
            raise MovieNotFoundError(status_code=404, detail="Movie not found") from e

        screenings = [
            Screening(
                screening_id=None,
                movie_id=dto.movie_id,
                hall_id=dto.hall_id,
                starts_at=dto.starts_at[i],
                ends_at=dto.starts_at[i] + timedelta(minutes=movie.duration),
                price_normal=dto.price_normal,
                price_vip=dto.price_vip,
                status=dto.status,
            )
            for i in range(len(dto.starts_at))
        ]

        try:
            screening_ids = await self._screening_repository.create_screenings(
                screenings=screenings
            )

        except IntegrityError as e:
            if "movie_id" in str(e.orig):
                raise MovieNotFoundError(
                    status_code=404, detail="Movie not found"
                ) from e
            elif "hall_id" in str(e.orig):
                raise HallNotFoundError(status_code=404, detail="Hall not found") from e

        seat_ids = await self._hall_repository.fetch_seat_ids(hall_id=dto.hall_id)

        screening_seats = [
            ScreeningSeat(
                screening_id=screening_id,
                seat_id=seat_id,
                reservation_id=None,
                status="free",
            )
            for screening_id in screening_ids
            for seat_id in seat_ids
        ]

        await self._screening_seat_repository.create_screening_seats(
            screening_seats=screening_seats
        )

        return screening_ids

    async def delete_screening(self, screening_id: int, user_role: str) -> None:
        self._user_role_check(user_role)

        result = await self._screening_repository.delete_screening(screening_id)

        if not result:
            raise ScreeningNotFoundError(
                status_code=404, detail="Screening does not exist"
            )

    async def update_screening(
        self, screening_id: int, dto: UpdateScreeningDTO, user_role: str
    ) -> None:
        self._user_role_check(user_role)

        screening = await self._screening_repository.fetch_basic_screening(
            screening_id=screening_id
        )
        updated_screening = screening.update_fields(**asdict(dto))

        try:
            await self._screening_repository.save_screening(screening=updated_screening)
        except IntegrityError as e:
            if "movie_id" in str(e.orig):
                raise MovieNotFoundError(
                    status_code=404, detail="Movie not found"
                ) from e
            elif "hall_id" in str(e.orig):
                raise HallNotFoundError(status_code=404, detail="Hall not found") from e
            raise

    async def get_screening(self, screening_id: int) -> ScreeningDetailsDTO:
        screening_details = (
            await self._screening_repository.fetch_screening_with_relations(
                screening_id=screening_id
            )
        )

        if not screening_details:
            raise ScreeningNotFoundError(status_code=404, detail="Screening not found")

        return screening_details

    async def hold_seats(
        self, seat_ids: list[int], user_id: int, screening_id: int
    ) -> ReservationHoldDTO:
        screening = await self._screening_repository.fetch_screening_with_relations(
            screening_id=screening_id
        )
        if not screening:
            raise ScreeningNotFoundError(status_code=404, detail="Screening not found")

        seats_data = await self._screening_repository.fetch_seats_by_ids(
            screening_id=screening_id, seat_ids=seat_ids
        )

        found_ids = {s.seat_id for s in seats_data}
        missing = [sid for sid in seat_ids if sid not in found_ids]
        if missing:
            raise SeatUnavailableError(
                status_code=422,
                detail=f"Seats not found in this screening: {missing}",
            )

        reserved_by_row_number = {
            (s.row, s.number) for s in screening.seats if s.status == "reserved"
        }
        reserved_ids = [
            s.seat_id for s in seats_data if (s.row, s.number) in reserved_by_row_number
        ]
        if reserved_ids:
            raise SeatUnavailableError(
                status_code=409,
                detail=f"Seats already reserved: {reserved_ids}",
            )

        already_held = await self._redis_repository.are_seats_held(
            screening_id=screening_id, seat_ids=seat_ids
        )
        if already_held:
            raise SeatUnavailableError(
                status_code=409, detail=f"Seats already on hold: {already_held}"
            )

        hold_id, expires_at = await self._redis_repository.hold(
            user_id=user_id,
            seat_ids=seat_ids,
            screening_id=screening_id,
            seats_data=seats_data,
        )

        return ReservationHoldDTO(
            hold_id=hold_id,
            expires_at=expires_at,
            seats=seats_data,
            total_price=sum(s.price for s in seats_data),
        )

    async def release_hold(self, hold_id: int, user_id: int, screening_id: int) -> None:
        released = await self._redis_repository.release(
            hold_id=hold_id, user_id=user_id, screening_id=screening_id
        )
        if not released:
            raise ScreeningNotFoundError(
                status_code=404, detail="Hold not found or already expired"
            )
