import pytest


@pytest.fixture
def register_url() -> str:
    return "/api/v1/auth/register"


@pytest.fixture
def login_url() -> str:
    return "/api/v1/auth/login"


@pytest.fixture
def logout_url() -> str:
    return "/api/v1/auth/logout"


@pytest.fixture
def refresh_url() -> str:
    return "/api/v1/auth/refresh"


@pytest.fixture
def user_payload() -> dict:
    return {
        "email": "testuser@example.com",
        "password": "password123",
        "password_repeat": "password123",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
async def registered_user(client, register_url, user_payload) -> dict:
    response = await client.post(register_url, json=user_payload)
    return response.json()
