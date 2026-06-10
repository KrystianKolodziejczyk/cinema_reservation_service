from app.modules.cinema.application.dto import CreateReservationDTO
from app.modules.cinema.application.excpetions import ReservationDataNotFoundError
from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.domain.entities import Reservation
from app.modules.cinema.infrastructure.interface import IReservationRepository
from app.modules.cinema.infrastructure.repository import ReservationHoldRepository
from app.modules.shared.exceptions import InvalidDataError


class ReservationService(IReservationService):
    def __init__(
        self,
        repository: IReservationRepository,
        redis_repository: ReservationHoldRepository,
    ) -> None:
        self._repository = repository
        self._redis_repository = redis_repository

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

        await self._repository.save_reservation(reservation=reservation)
