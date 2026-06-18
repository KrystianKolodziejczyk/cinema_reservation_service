from unittest.mock import AsyncMock

import pytest

from app.modules.cinema.application.dto import AddScreeningDTO, ScreeningDetailsDTO, UpdateScreeningDTO
from app.modules.cinema.application.excpetions import (
    PermissionDeniedError,
    ScreeningNotFoundError,
    SeatUnavailableError,
)
from app.modules.cinema.application.service.screening_service import ScreeningService

pytestmark = pytest.mark.anyio


class TestScreeningServiceExceptions:
    async def test_raises_permission_denied_on_add(
        self,
        screening_service: ScreeningService,
        add_screening_dto: AddScreeningDTO,
    ):
        with pytest.raises(PermissionDeniedError):
            await screening_service.add_screening(dto=add_screening_dto, user_role="client")

    async def test_raises_permission_denied_on_delete(
        self, screening_service: ScreeningService
    ):
        with pytest.raises(PermissionDeniedError):
            await screening_service.delete_screening(screening_id=1, user_role="client")

    async def test_raises_screening_not_found_on_delete(
        self,
        screening_service: ScreeningService,
        mock_screening_repository: AsyncMock,
    ):
        mock_screening_repository.delete_screening.return_value = False

        with pytest.raises(ScreeningNotFoundError):
            await screening_service.delete_screening(screening_id=99999, user_role="admin")

    async def test_raises_screening_not_found_on_update(
        self,
        screening_service: ScreeningService,
        mock_screening_repository: AsyncMock,
    ):
        mock_screening_repository.fetch_basic_screening.return_value = None

        with pytest.raises(ScreeningNotFoundError):
            await screening_service.update_screening(
                screening_id=99999,
                dto=UpdateScreeningDTO(price_normal=30, price_vip=40),
                user_role="admin",
            )

    async def test_raises_screening_not_found_on_get(
        self,
        screening_service: ScreeningService,
        mock_screening_repository: AsyncMock,
    ):
        mock_screening_repository.fetch_screening_with_relations.return_value = None

        with pytest.raises(ScreeningNotFoundError):
            await screening_service.get_screening(screening_id=99999)

    async def test_raises_screening_not_found_on_hold(
        self,
        screening_service: ScreeningService,
        mock_screening_repository: AsyncMock,
    ):
        mock_screening_repository.fetch_screening_with_relations.return_value = None

        with pytest.raises(ScreeningNotFoundError):
            await screening_service.hold_seats(seat_ids=[1], user_id=1, screening_id=99999)

    async def test_raises_seat_unavailable_when_seats_not_in_screening(
        self,
        screening_service: ScreeningService,
        mock_screening_repository: AsyncMock,
        screening_details_dto: ScreeningDetailsDTO,
    ):
        mock_screening_repository.fetch_screening_with_relations.return_value = screening_details_dto
        mock_screening_repository.fetch_seats_by_ids.return_value = []

        with pytest.raises(SeatUnavailableError):
            await screening_service.hold_seats(seat_ids=[999], user_id=1, screening_id=1)
