import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


class TestAddHall:
    async def test_add_hall_success(
        self,
        client: AsyncClient,
        halls_url: str,
        hall_payload: dict[str, str | int],
        admin_token: str,
    ):
        response = await client.post(
            halls_url, json=hall_payload, headers={"Authorization": admin_token}
        )

        assert response.status_code == 201
        assert "hall_id" in response.json()

    async def test_add_hall_permission_denied(
        self,
        client: AsyncClient,
        halls_url: str,
        hall_payload: dict[str, str | int],
        client_token: str,
    ):
        response = await client.post(
            halls_url, json=hall_payload, headers={"Authorization": client_token}
        )

        assert response.status_code == 403


class TestDeleteHall:
    async def test_delete_hall_success(
        self, client: AsyncClient, halls_url: str, created_hall: dict, admin_token: str
    ):
        hall_id = created_hall["hall_id"]
        response = await client.delete(
            f"{halls_url}/{hall_id}", headers={"Authorization": admin_token}
        )

        assert response.status_code == 204

    async def test_delete_hall_not_found(
        self, client: AsyncClient, halls_url: str, admin_token: str
    ):
        response = await client.delete(
            f"{halls_url}/99999", headers={"Authorization": admin_token}
        )

        assert response.status_code == 404

    async def test_delete_hall_permission_denied(
        self, client: AsyncClient, halls_url: str, created_hall: dict, client_token: str
    ):
        hall_id = created_hall["hall_id"]
        response = await client.delete(
            f"{halls_url}/{hall_id}", headers={"Authorization": client_token}
        )

        assert response.status_code == 403
