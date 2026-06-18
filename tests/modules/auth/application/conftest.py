import pytest
from unittest.mock import AsyncMock

from app.modules.auth.infrastructure.interface.i_auth_repository import IAuthRepository


@pytest.fixture
def mock_repository() -> AsyncMock:
    return AsyncMock(spec=IAuthRepository)
