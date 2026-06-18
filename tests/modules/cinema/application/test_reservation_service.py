from unittest.mock import AsyncMock

import pytest

from app.modules.cinema.application.dto import (
    CreateReservationDTO,
    HoldDTO,
    ReservationDTO,
)
from app.modules.cinema.application.excpetions import (
    PermissionDeniedError,
    ReservationCancellationError,
    ReservationDataNotFoundError,
    ReservationMismatchError,
    ReservationNotFoundError,
    ScreeningNotAvailableError,
)
from app.modules.cinema.application.service import ReservationService
from app.modules.cinema.domain.entities import Screening

pytestmark = pytest.mark.anyio


class TestReservationServiceExceptions:
    async def test_raises_reservation_data_not_found(
        self,
        reservation_service: ReservationService,
        mock_reservation_hold_repository: AsyncMock,
    ):
        mock_reservation_hold_repository.get_hold.return_value = None
        dto = CreateReservationDTO(hold_id=99, screening_id=1)

        with pytest.raises(ReservationDataNotFoundError):
            await reservation_service.create_reservation(user_id=1, dto=dto)

    async def test_raises_screening_not_available(
        self,
        reservation_service: ReservationService,
        mock_reservation_hold_repository: AsyncMock,
        mock_screening_repository: AsyncMock,
        hold_dto: HoldDTO,
        ongoing_screening: Screening,
    ):
        mock_reservation_hold_repository.get_hold.return_value = hold_dto
        mock_screening_repository.fetch_basic_screening.return_value = ongoing_screening
        dto = CreateReservationDTO(hold_id=1, screening_id=1)

        with pytest.raises(ScreeningNotAvailableError):
            await reservation_service.create_reservation(user_id=1, dto=dto)

    async def test_raises_reservation_not_found_on_get(
        self,
        reservation_service: ReservationService,
        mock_reservation_repository: AsyncMock,
    ):
        mock_reservation_repository.fetch_reservation.return_value = None

        with pytest.raises(ReservationNotFoundError):
            await reservation_service.get_reservation(
                reservation_id=99999, user_data={"user_id": 1, "role": "client"}
            )

    async def test_raises_permission_denied_on_get_other_user(
        self,
        reservation_service: ReservationService,
        mock_reservation_repository: AsyncMock,
        reservation_dto: ReservationDTO,
    ):
        mock_reservation_repository.fetch_reservation.return_value = reservation_dto

        with pytest.raises(PermissionDeniedError):
            await reservation_service.get_reservation(
                reservation_id=1, user_data={"user_id": 1, "role": "client"}
            )

    async def test_raises_reservation_cancellation_error_on_ongoing_screening(
        self,
        reservation_service: ReservationService,
        mock_screening_repository: AsyncMock,
        ongoing_screening: Screening,
    ):
        mock_screening_repository.get_screening_for_reservation.return_value = (
            ongoing_screening
        )

        with pytest.raises(ReservationCancellationError):
            await reservation_service.cancel_reservation(
                reservation_id=1, user_data={"user_id": 1, "role": "client"}
            )

    async def test_raises_reservation_mismatch_when_screening_not_found(
        self,
        reservation_service: ReservationService,
        mock_screening_repository: AsyncMock,
    ):
        mock_screening_repository.get_screening_for_reservation.return_value = None

        with pytest.raises(ReservationMismatchError):
            await reservation_service.cancel_reservation(
                reservation_id=1, user_data={"user_id": 1, "role": "client"}
            )
