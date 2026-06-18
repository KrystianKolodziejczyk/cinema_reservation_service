import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


class TestAddScreening:
    async def test_add_screening_success(
        self,
        client: AsyncClient,
        screenings_url: str,
        screening_payload: dict[str, str | int | list],
        admin_token: str,
    ):
        response = await client.post(
            screenings_url,
            json=screening_payload,
            headers={"Authorization": admin_token},
        )

        assert response.status_code == 201
        assert "screening_ids" in response.json()
        assert len(response.json()["screening_ids"]) == 1

    async def test_add_screening_permission_denied(
        self,
        client: AsyncClient,
        screenings_url: str,
        screening_payload: dict[str, str | int | list],
        client_token: str,
    ):
        response = await client.post(
            screenings_url,
            json=screening_payload,
            headers={"Authorization": client_token},
        )

        assert response.status_code == 403


class TestGetScreening:
    async def test_get_screening_success(
        self, client: AsyncClient, screenings_url: str, created_screening: dict
    ):
        screening_id = created_screening["screening_ids"][0]
        response = await client.get(f"{screenings_url}/{screening_id}")

        assert response.status_code == 200
        assert response.json()["screening_id"] == screening_id

    async def test_get_screening_not_found(
        self, client: AsyncClient, screenings_url: str
    ):
        response = await client.get(f"{screenings_url}/99999")

        assert response.status_code == 404


class TestUpdateScreening:
    async def test_update_screening_success(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        admin_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]
        response = await client.put(
            f"{screenings_url}/{screening_id}",
            json={"price_normal": 30, "price_vip": 40},
            headers={"Authorization": admin_token},
        )

        assert response.status_code == 204

    async def test_update_screening_not_found(
        self, client: AsyncClient, screenings_url: str, admin_token: str
    ):
        response = await client.put(
            f"{screenings_url}/99999",
            json={"price_normal": 30, "price_vip": 40},
            headers={"Authorization": admin_token},
        )

        assert response.status_code == 404

    async def test_update_screening_permission_denied(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]
        response = await client.put(
            f"{screenings_url}/{screening_id}",
            json={"price_normal": 30, "price_vip": 40},
            headers={"Authorization": client_token},
        )

        assert response.status_code == 403


class TestDeleteScreening:
    async def test_delete_screening_success(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        admin_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]
        response = await client.delete(
            f"{screenings_url}/{screening_id}", headers={"Authorization": admin_token}
        )

        assert response.status_code == 204

    async def test_delete_screening_not_found(
        self, client: AsyncClient, screenings_url: str, admin_token: str
    ):
        response = await client.delete(
            f"{screenings_url}/99999", headers={"Authorization": admin_token}
        )

        assert response.status_code == 404

    async def test_delete_screening_permission_denied(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]
        response = await client.delete(
            f"{screenings_url}/{screening_id}", headers={"Authorization": client_token}
        )

        assert response.status_code == 403


class TestHoldSeats:
    async def test_hold_seats_success(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]

        screening_response = await client.get(f"{screenings_url}/{screening_id}")
        seat_ids = [screening_response.json()["seats"][0]["seat_id"]]

        response = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": seat_ids},
            headers={"Authorization": client_token},
        )

        assert response.status_code == 200
        assert "hold_id" in response.json()

    async def test_hold_already_held_seats(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]

        screening_response = await client.get(f"{screenings_url}/{screening_id}")
        seat_ids = [screening_response.json()["seats"][0]["seat_id"]]

        await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": seat_ids},
            headers={"Authorization": client_token},
        )

        response = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": seat_ids},
            headers={"Authorization": client_token},
        )

        assert response.status_code == 409

    async def test_hold_seats_screening_not_found(
        self, client: AsyncClient, screenings_url: str, client_token: str
    ):
        response = await client.post(
            f"{screenings_url}/99999/seats/hold",
            json={"seat_ids": [1]},
            headers={"Authorization": client_token},
        )

        assert response.status_code == 404


class TestReleaseHold:
    async def test_release_hold_success(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]

        screening_response = await client.get(f"{screenings_url}/{screening_id}")
        seat_ids = [screening_response.json()["seats"][0]["seat_id"]]

        hold_response = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": seat_ids},
            headers={"Authorization": client_token},
        )
        hold_id = hold_response.json()["hold_id"]

        response = await client.delete(
            f"{screenings_url}/{screening_id}/seats/hold/{hold_id}",
            headers={"Authorization": client_token},
        )

        assert response.status_code == 204

    async def test_release_hold_not_found(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]

        response = await client.delete(
            f"{screenings_url}/{screening_id}/seats/hold/99999",
            headers={"Authorization": client_token},
        )

        assert response.status_code == 404
