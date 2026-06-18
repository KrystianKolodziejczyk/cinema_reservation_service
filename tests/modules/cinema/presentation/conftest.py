from datetime import datetime, timedelta

import jwt
import pytest
from httpx import AsyncClient

from app.modules.shared.config.settings import settings


@pytest.fixture
def admin_token() -> str:
    payload = {
        "sub": "999",
        "iat": datetime.now().timestamp(),
        "exp": (datetime.now() + timedelta(minutes=15)).timestamp(),
        "role": "admin",
    }
    return jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")


@pytest.fixture
def client_token() -> str:
    payload = {
        "sub": "998",
        "iat": datetime.now().timestamp(),
        "exp": (datetime.now() + timedelta(minutes=15)).timestamp(),
        "role": "client",
    }
    return jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")


@pytest.fixture
def movies_url() -> str:
    return "/api/v1/movies"


@pytest.fixture
def movie_payload() -> dict:
    return {
        "title": "Test Movie",
        "description": "A test movie description",
        "director": "Test Director",
        "duration": 120,
        "genre": "drama",
        "rating": 4.5,
        "poster_url": None,
    }


@pytest.fixture
async def created_movie(client, movies_url, movie_payload, admin_token) -> dict:
    response = await client.post(
        movies_url, json=movie_payload, headers={"Authorization": admin_token}
    )
    return response.json()


@pytest.fixture
def halls_url() -> str:
    return "/api/v1/halls"


@pytest.fixture
def hall_payload() -> dict[str, str | int]:
    return {"hall_name": "Hall A", "rows": 5, "seats_per_row": 10}


@pytest.fixture
async def created_hall(client, halls_url, hall_payload, admin_token) -> dict:
    response = await client.post(
        halls_url, json=hall_payload, headers={"Authorization": admin_token}
    )
    return response.json()


@pytest.fixture
def screenings_url() -> str:
    return "/api/v1/screenings"


@pytest.fixture
async def screening_payload(
    created_movie: dict, created_hall: dict
) -> dict[str, str | int | list]:
    return {
        "movie_id": created_movie["movie_id"],
        "hall_id": created_hall["hall_id"],
        "starts_at": ["2026-12-01T10:00:00"],
        "price_normal": 25,
        "price_vip": 35,
    }


@pytest.fixture
async def created_screening(
    client, screenings_url, screening_payload, admin_token
) -> dict:
    response = await client.post(
        screenings_url, json=screening_payload, headers={"Authorization": admin_token}
    )
    return response.json()


@pytest.fixture
async def ongoing_screening_payload(
    created_movie: dict, created_hall: dict
) -> dict[str, str | int | list]:
    starts_at = (datetime.now() - timedelta(minutes=30)).isoformat()
    return {
        "movie_id": created_movie["movie_id"],
        "hall_id": created_hall["hall_id"],
        "starts_at": [starts_at],
        "price_normal": 25,
        "price_vip": 35,
    }


@pytest.fixture
def reservations_url() -> str:
    return "/api/v1/reservations"


@pytest.fixture
async def registered_client_token(client: AsyncClient) -> str:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "client1@test.com",
            "password": "password123",
            "password_repeat": "password123",
            "first_name": "Client",
            "last_name": "One",
        },
    )
    return response.json()["access_token"]


@pytest.fixture
async def second_client_token(client: AsyncClient) -> str:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "client2@test.com",
            "password": "password123",
            "password_repeat": "password123",
            "first_name": "Client",
            "last_name": "Two",
        },
    )
    return response.json()["access_token"]


@pytest.fixture
async def active_hold(
    client: AsyncClient,
    screenings_url: str,
    created_screening: dict,
    registered_client_token: str,
) -> dict:
    screening_id = created_screening["screening_ids"][0]
    screening_response = await client.get(f"{screenings_url}/{screening_id}")
    seat_id = screening_response.json()["seats"][0]["seat_id"]

    response = await client.post(
        f"{screenings_url}/{screening_id}/seats/hold",
        json={"seat_ids": [seat_id]},
        headers={"Authorization": registered_client_token},
    )
    return {**response.json(), "screening_id": screening_id}


@pytest.fixture
async def created_reservation(
    client: AsyncClient,
    reservations_url: str,
    active_hold: dict,
    registered_client_token: str,
) -> dict:
    response = await client.post(
        reservations_url,
        json={
            "hold_id": active_hold["hold_id"],
            "screening_id": active_hold["screening_id"],
        },
        headers={"Authorization": registered_client_token},
    )
    return response.json()
