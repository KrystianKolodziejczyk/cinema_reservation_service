from sqlalchemy.exc import IntegrityError

from app.modules.cinema.application.dto import CreateReservationDTO, ReservationDTO
from app.modules.cinema.application.excpetions import (
    PermissionDeniedError,
    ReservationCancellationError,
    ReservationDataNotFoundError,
    ReservationMismatchError,
    ReservationNotFoundError,
    ScreeningNotAvailableError,
)
from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.domain.entities import Reservation
from app.modules.cinema.infrastructure.interface import (
    IReservationHoldRepository,
    IReservationRepository,
    IScreeningRepository,
    IScreeningSeatRepository,
)
from app.modules.shared.exceptions import InvalidDataError


class ReservationService(IReservationService):
    def __init__(
        self,
        reservation_repository: IReservationRepository,
        redis_repository: IReservationHoldRepository,
        screening_seat_repository: IScreeningSeatRepository,
        screening_repository: IScreeningRepository,
    ) -> None:
        self._reservation_repository = reservation_repository
        self._redis_repository = redis_repository
        self._screening_seat_repository = screening_seat_repository
        self._screening_repository = screening_repository

    async def create_reservation(self, user_id: int, dto: CreateReservationDTO) -> int:
        hold_data = await self._redis_repository.get_hold(
            hold_id=dto.hold_id, user_id=user_id
        )

        if not hold_data:
            raise ReservationDataNotFoundError(
                status_code=404, detail="Reservation data not found"
            )

        if hold_data.screening_id != dto.screening_id:
            raise InvalidDataError(status_code=409, detail="Incompatible data")

        reservation = Reservation(
            reservation_id=None,
            user_id=user_id,
            screening_id=hold_data.screening_id,
            status="confirmed",
            total_price=hold_data.total_price,
        )

        screening = await self._screening_repository.fetch_basic_screening(
            screening_id=reservation.screening_id
        )

        if not screening:
            raise ScreeningNotAvailableError(
                status_code=404, detail="Screening not found"
            )

        if screening.status in {"ongoing", "completed", "cancelled"}:
            raise ScreeningNotAvailableError(
                status_code=409, detail="Screening not available"
            )

        try:
            reservation_id = await self._reservation_repository.save_reservation(
                reservation=reservation
            )
        except IntegrityError as e:
            raise InvalidDataError(status_code=409, detail="Incompatible data") from e

        await self._reservation_repository.save_reserved_seats(
            seats=hold_data.seats, reservation_id=reservation_id
        )

        await self._screening_seat_repository.set_seat_as_reserved(
            reservation_id=reservation_id,
            seat_ids=[seat.seat_id for seat in hold_data.seats],
            screening_id=reservation.screening_id,
        )

        await self._redis_repository.release(
            hold_id=hold_data.hold_id,
            user_id=user_id,
            screening_id=reservation.screening_id,
        )

        return await self._reservation_repository.fetch_reservation(
            reservation_id=reservation_id
        )

    async def get_reservation(
        self, reservation_id: int, user_data: dict[str, str | int]
    ) -> ReservationDTO:
        reservation_details = await self._reservation_repository.fetch_reservation(
            reservation_id=reservation_id
        )

        if reservation_details is None:
            raise ReservationNotFoundError(
                status_code=404, detail="Reservation not found"
            )

        if (
            user_data["role"] != "admin"
            and reservation_details.user_id != user_data["user_id"]
        ):
            raise PermissionDeniedError(status_code=403, detail="Permission denied")

        return reservation_details

    async def cancel_reservation(self, reservation_id: int, user_data: dict) -> None:
        if user_data["role"] == "admin":
            await self._release_reservation_everywhere(reservation_id=reservation_id)
            return

        screening = await self._screening_repository.get_screening_for_reservation(
            reservation_id=reservation_id, user_id=user_data["user_id"]
        )

        if not screening:
            raise ReservationMismatchError(
                status_code=409, detail="Wrong reservation_id or user_id"
            )

        if screening.status != "scheduled":
            raise ReservationCancellationError(
                status_code=409,
                detail="Can not cancell reservation during or after screening",
            )

        await self._release_reservation_everywhere(
            reservation_id=reservation_id, user_id=user_data["user_id"]
        )

    async def _release_reservation_everywhere(
        self, reservation_id: int, user_id: int | None = None
    ) -> None:
        status_change_result = (
            await self._reservation_repository.change_reservation_status(
                reservation_id=reservation_id, user_id=user_id
            )
        )
        if not status_change_result:
            raise ReservationMismatchError(
                status_code=409, detail="Wrong reservation_id or user_id"
            )

        await self._screening_seat_repository.release_screening_seats(
            reservation_id=reservation_id
        )

    async def get_reservation_history(
        self, user_id: int, page: int = 1, limit: int = 20
    ) -> tuple[list[ReservationDTO | None], int]:
        return await self._reservation_repository.fetch_reservations_for_user(
            user_id=user_id, page=page, limit=limit
        )
