from sqlalchemy.exc import IntegrityError

from app.modules.cinema.application.dto import CreateReservationDTO, GetReservationDTO
from app.modules.cinema.application.excpetions import (
    ReservationDataNotFoundError,
    ReservationNotFoundError,
)
from app.modules.cinema.application.excpetions.permission_denied_error import (
    PermissionDeniedError,
)
from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.domain.entities import Reservation
from app.modules.cinema.infrastructure.interface import (
    IReservationHoldRepository,
    IReservationRepository,
    IScreeningSeatRepository,
)
from app.modules.shared.exceptions import InvalidDataError


class ReservationService(IReservationService):
    def __init__(
        self,
        reservation_repository: IReservationRepository,
        redis_repository: IReservationHoldRepository,
        screening_seat_repository: IScreeningSeatRepository,
    ) -> None:
        self._reservation_repository = reservation_repository
        self._redis_repository = redis_repository
        self._screening_seat_repository = screening_seat_repository

    async def create_reservation(self, user_id: int, dto: CreateReservationDTO) -> None:
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
            conf_code="example",
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
        )

        await self._redis_repository.release(
            hold_id=hold_data.hold_id,
            user_id=user_id,
            screening_id=hold_data.screening_id,
        )

    async def get_reservation(
        self, reservation_id: int, user_data: dict[str, str | int]
    ) -> GetReservationDTO:
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
