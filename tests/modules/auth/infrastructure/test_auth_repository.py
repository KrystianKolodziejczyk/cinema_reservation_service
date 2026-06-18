from datetime import datetime, timedelta

import pytest

from app.modules.auth.domain.entities import RefreshToken, User
from app.modules.auth.infrastructure.interface.i_auth_repository import IAuthRepository

pytestmark = pytest.mark.anyio


class TestAuthRepository:
    async def test_save_and_fetch_user(self, auth_repository: IAuthRepository):
        user = User(
            user_id=None,
            email="repo_test@example.com",
            password="hashed_password_value",
            first_name="Jane",
            last_name="Smith",
        )
        user_id = await auth_repository.save_user(user=user)

        assert isinstance(user_id, int)
        fetched = await auth_repository.fetch_user(email="repo_test@example.com")
        assert fetched._user_id == user_id
        assert fetched._email == "repo_test@example.com"

    async def test_fetch_user_returns_none_when_not_found(self, auth_repository: IAuthRepository):
        result = await auth_repository.fetch_user(email="nobody@example.com")

        assert result is None

    async def test_save_and_fetch_refresh_token(self, auth_repository: IAuthRepository):
        user = User(
            user_id=None,
            email="token_test@example.com",
            password="hashed_password_value",
            first_name="Token",
            last_name="Test",
        )
        user_id = await auth_repository.save_user(user=user)

        token = RefreshToken(
            refresh_token_id=None,
            user_id=user_id,
            token_hash="test_hash_abc123",
            expires_at=datetime.now() + timedelta(days=7),
        )
        await auth_repository.save_refresh_token(refresh_token=token)

        fetched = await auth_repository.fetch_refresh_token(user_id=user_id, token="test_hash_abc123")
        assert fetched is not None
        assert fetched.token_hash == "test_hash_abc123"
        assert fetched.user_id == user_id

    async def test_delete_refresh_token(self, auth_repository: IAuthRepository):
        user = User(
            user_id=None,
            email="delete_test@example.com",
            password="hashed_password_value",
            first_name="Delete",
            last_name="Test",
        )
        user_id = await auth_repository.save_user(user=user)

        token = RefreshToken(
            refresh_token_id=None,
            user_id=user_id,
            token_hash="delete_hash_xyz",
            expires_at=datetime.now() + timedelta(days=7),
        )
        await auth_repository.save_refresh_token(refresh_token=token)

        saved = await auth_repository.fetch_refresh_token(user_id=user_id, token="delete_hash_xyz")
        await auth_repository.delete_refresh_token(
            user_id=user_id, refresh_token_id=saved.refresh_token_id
        )

        result = await auth_repository.fetch_refresh_token(user_id=user_id, token="delete_hash_xyz")
        assert result is None
