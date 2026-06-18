from unittest.mock import AsyncMock

import pytest

from app.modules.auth.infrastructure.interface import IAuthRepository


@pytest.fixture
def mock_repository() -> AsyncMock:
    return AsyncMock(spec=IAuthRepository)
