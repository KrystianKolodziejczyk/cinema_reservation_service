from unittest.mock import AsyncMock

import pytest

from app.modules.cinema.application.dto import AddHallDTO
from app.modules.cinema.application.excpetions import HallNotFoundError, PermissionDeniedError
from app.modules.cinema.application.service.hall_service import HallService

pytestmark = pytest.mark.anyio


class TestHallServiceExceptions:
    async def test_raises_permission_denied_on_add(
        self, mock_hall_repository: AsyncMock
    ):
        service = HallService(repository=mock_hall_repository)
        dto = AddHallDTO(hall_name="Hall A", rows=5, seats_per_row=10)

        with pytest.raises(PermissionDeniedError):
            await service.add_hall(dto=dto, user_role="client")

    async def test_raises_permission_denied_on_delete(
        self, mock_hall_repository: AsyncMock
    ):
        service = HallService(repository=mock_hall_repository)

        with pytest.raises(PermissionDeniedError):
            await service.delete_hall(hall_id=1, user_role="client")

    async def test_raises_hall_not_found_on_delete(
        self, mock_hall_repository: AsyncMock
    ):
        mock_hall_repository.delete_hall.return_value = False
        service = HallService(repository=mock_hall_repository)

        with pytest.raises(HallNotFoundError):
            await service.delete_hall(hall_id=99999, user_role="admin")
