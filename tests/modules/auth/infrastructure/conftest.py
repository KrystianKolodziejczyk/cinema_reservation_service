import pytest

from app.modules.auth.infrastructure.repository import AuthRepository


@pytest.fixture
def auth_repository(db_session) -> AuthRepository:
    return AuthRepository(session=db_session)
