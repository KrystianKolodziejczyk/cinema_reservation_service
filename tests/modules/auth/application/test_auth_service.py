from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.modules.auth.application.dto import LoginDTO, RegisterUserDTO
from app.modules.auth.application.exceptions import (
    DifferentPasswordsError,
    DuplicateEmailError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
    WrongPasswordError,
)
from app.modules.auth.application.service import AuthService
from app.modules.auth.domain.entities import RefreshToken, User
from app.modules.shared.exceptions import InvalidTokenError

pytestmark = pytest.mark.anyio


class TestAuthServiceExceptions:
    async def test_raises_different_passwords_error(self, mock_repository: AsyncMock):
        service = AuthService(repository=mock_repository)
        dto = RegisterUserDTO(
            email="test@example.com",
            password="password123",
            password_repeat="different123",
            first_name="John",
            last_name="Doe",
        )

        with pytest.raises(DifferentPasswordsError):
            await service.register_user(dto=dto)

    async def test_raises_duplicate_email_error(self, mock_repository: AsyncMock):
        mock_repository.save_user.side_effect = IntegrityError(
            None, None, Exception("unique constraint")
        )
        service = AuthService(repository=mock_repository)
        dto = RegisterUserDTO(
            email="test@example.com",
            password="password123",
            password_repeat="password123",
            first_name="John",
            last_name="Doe",
        )

        with pytest.raises(DuplicateEmailError):
            await service.register_user(dto=dto)

    async def test_raises_user_not_found_error(self, mock_repository: AsyncMock):
        mock_repository.fetch_user.return_value = None
        service = AuthService(repository=mock_repository)
        dto = LoginDTO(email="nobody@example.com", password="password123")

        with pytest.raises(UserNotFoundError):
            await service.login(dto=dto)

    async def test_raises_wrong_password_error(self, mock_repository: AsyncMock):
        user = User(
            user_id=1,
            email="test@example.com",
            password="correct_password",
            first_name="John",
            last_name="Doe",
        )
        user.hash_password()
        mock_repository.fetch_user.return_value = user
        service = AuthService(repository=mock_repository)
        dto = LoginDTO(email="test@example.com", password="wrong_password")

        with pytest.raises(WrongPasswordError):
            await service.login(dto=dto)

    async def test_raises_invalid_token_error(self, mock_repository: AsyncMock):
        service = AuthService(repository=mock_repository)

        with pytest.raises(InvalidTokenError):
            await service.logout("not.a.valid.jwt.token")

    async def test_raises_refresh_token_not_found_error(
        self, mock_repository: AsyncMock
    ):
        mock_repository.fetch_refresh_token.return_value = None
        service = AuthService(repository=mock_repository)
        token, _ = service._create_refresh_token(user_id=1, role="client")

        with pytest.raises(RefreshTokenNotFoundError):
            await service.logout(token)

    async def test_raises_refresh_token_expired_error(self, mock_repository: AsyncMock):
        service = AuthService(repository=mock_repository)
        token, _ = service._create_refresh_token(user_id=1, role="client")

        expired_token = RefreshToken(
            refresh_token_id=1,
            user_id=1,
            token_hash=service._hash_token(token),
            expires_at=datetime.now() - timedelta(days=1),
        )
        mock_repository.fetch_refresh_token.return_value = expired_token

        with pytest.raises(RefreshTokenExpiredError):
            await service.logout(token)
