import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


class TestGetMovies:
    async def test_get_movies_empty(self, client: AsyncClient, movies_url: str):
        response = await client.get(movies_url)

        assert response.status_code == 200
        assert response.json()["total"] == 0
        assert response.json()["items"] == []

    async def test_get_movies_returns_items(
        self, client: AsyncClient, movies_url: str, created_movie: dict
    ):
        response = await client.get(movies_url)

        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["items"][0]["movie_id"] == created_movie["movie_id"]


class TestAddMovie:
    async def test_add_movie_success(
        self,
        client: AsyncClient,
        movies_url: str,
        movie_payload: dict[str, str | int | float | None],
        admin_token: str,
    ):
        response = await client.post(
            movies_url, json=movie_payload, headers={"Authorization": admin_token}
        )

        assert response.status_code == 201
        assert "movie_id" in response.json()

    async def test_add_movie_permission_denied(
        self,
        client: AsyncClient,
        movies_url: str,
        movie_payload: dict[str, str | int | float | None],
        client_token: str,
    ):
        response = await client.post(
            movies_url, json=movie_payload, headers={"Authorization": client_token}
        )

        assert response.status_code == 403


class TestGetMovie:
    async def test_get_movie_success(
        self, client: AsyncClient, movies_url: str, created_movie: dict
    ):
        movie_id = created_movie["movie_id"]
        response = await client.get(f"{movies_url}/{movie_id}")

        assert response.status_code == 200
        assert response.json()["movie_id"] == movie_id

    async def test_get_movie_not_found(self, client: AsyncClient, movies_url: str):
        response = await client.get(f"{movies_url}/99999")

        assert response.status_code == 404


class TestDeleteMovie:
    async def test_delete_movie_success(
        self, client: AsyncClient, movies_url: str, created_movie: dict, admin_token: str
    ):
        movie_id = created_movie["movie_id"]
        response = await client.delete(
            f"{movies_url}/{movie_id}", headers={"Authorization": admin_token}
        )

        assert response.status_code == 204

    async def test_delete_movie_not_found(
        self, client: AsyncClient, movies_url: str, admin_token: str
    ):
        response = await client.delete(
            f"{movies_url}/99999", headers={"Authorization": admin_token}
        )

        assert response.status_code == 404

    async def test_delete_movie_permission_denied(
        self, client: AsyncClient, movies_url: str, created_movie: dict, client_token: str
    ):
        movie_id = created_movie["movie_id"]
        response = await client.delete(
            f"{movies_url}/{movie_id}", headers={"Authorization": client_token}
        )

        assert response.status_code == 403


class TestGetScreeningsForMovie:
    async def test_get_screenings_not_found(
        self, client: AsyncClient, movies_url: str, created_movie: dict
    ):
        movie_id = created_movie["movie_id"]
        response = await client.get(f"{movies_url}/{movie_id}/screenings")

        assert response.status_code == 404
