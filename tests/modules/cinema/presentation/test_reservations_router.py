import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


class TestCreateReservation:
    async def test_create_reservation_success(
        self,
        client: AsyncClient,
        reservations_url: str,
        active_hold: dict,
        registered_client_token: str,
    ):
        response = await client.post(
            reservations_url,
            json={
                "hold_id": active_hold["hold_id"],
                "screening_id": active_hold["screening_id"],
            },
            headers={"Authorization": registered_client_token},
        )

        assert response.status_code == 201
        assert "reservation_id" in response.json()

    async def test_create_reservation_screening_not_available(
        self,
        client: AsyncClient,
        reservations_url: str,
        screenings_url: str,
        ongoing_screening_payload: dict,
        admin_token: str,
        registered_client_token: str,
    ):
        ongoing_screening = await client.post(
            screenings_url,
            json=ongoing_screening_payload,
            headers={"Authorization": admin_token},
        )
        screening_id = ongoing_screening.json()["screening_ids"][0]

        screening_response = await client.get(f"{screenings_url}/{screening_id}")
        seat_id = screening_response.json()["seats"][0]["seat_id"]

        hold_response = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": [seat_id]},
            headers={"Authorization": registered_client_token},
        )

        response = await client.post(
            reservations_url,
            json={
                "hold_id": hold_response.json()["hold_id"],
                "screening_id": screening_id,
            },
            headers={"Authorization": registered_client_token},
        )

        assert response.status_code == 409


class TestGetReservation:
    async def test_get_reservation_success(
        self,
        client: AsyncClient,
        reservations_url: str,
        created_reservation: dict,
        registered_client_token: str,
    ):
        reservation_id = created_reservation["reservation_id"]
        response = await client.get(
            f"{reservations_url}/{reservation_id}",
            headers={"Authorization": registered_client_token},
        )

        assert response.status_code == 200
        assert response.json()["reservation_id"] == reservation_id

    async def test_get_reservation_not_found(
        self,
        client: AsyncClient,
        reservations_url: str,
        registered_client_token: str,
    ):
        response = await client.get(
            f"{reservations_url}/99999",
            headers={"Authorization": registered_client_token},
        )

        assert response.status_code == 404

    async def test_get_reservation_permission_denied_for_other_user(
        self,
        client: AsyncClient,
        reservations_url: str,
        created_reservation: dict,
        second_client_token: str,
    ):
        reservation_id = created_reservation["reservation_id"]
        response = await client.get(
            f"{reservations_url}/{reservation_id}",
            headers={"Authorization": second_client_token},
        )

        assert response.status_code == 403


class TestGetReservationHistory:
    async def test_get_reservation_history(
        self,
        client: AsyncClient,
        reservations_url: str,
        created_reservation: dict,
        registered_client_token: str,
    ):
        response = await client.get(
            f"{reservations_url}/me",
            headers={"Authorization": registered_client_token},
        )

        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert (
            response.json()["reservations"][0]["reservation_id"]
            == created_reservation["reservation_id"]
        )


class TestCancelReservation:
    async def test_cancel_reservation_success(
        self,
        client: AsyncClient,
        reservations_url: str,
        created_reservation: dict,
        registered_client_token: str,
    ):
        reservation_id = created_reservation["reservation_id"]
        response = await client.put(
            f"{reservations_url}/{reservation_id}",
            headers={"Authorization": registered_client_token},
        )

        assert response.status_code == 204

    async def test_cancel_reservation_mismatch(
        self,
        client: AsyncClient,
        reservations_url: str,
        created_reservation: dict,
        second_client_token: str,
    ):
        reservation_id = created_reservation["reservation_id"]
        response = await client.put(
            f"{reservations_url}/{reservation_id}",
            headers={"Authorization": second_client_token},
        )

        assert response.status_code == 409


class TestEdgeCases:
    async def test_two_users_cannot_hold_same_seats(
        self,
        client: AsyncClient,
        screenings_url: str,
        created_screening: dict,
        registered_client_token: str,
        second_client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]
        screening_response = await client.get(f"{screenings_url}/{screening_id}")
        seat_id = screening_response.json()["seats"][0]["seat_id"]

        await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": [seat_id]},
            headers={"Authorization": registered_client_token},
        )

        response = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": [seat_id]},
            headers={"Authorization": second_client_token},
        )

        assert response.status_code == 409

    async def test_cannot_reserve_already_reserved_seat(
        self,
        client: AsyncClient,
        screenings_url: str,
        reservations_url: str,
        created_screening: dict,
        registered_client_token: str,
        second_client_token: str,
    ):
        screening_id = created_screening["screening_ids"][0]
        screening_response = await client.get(f"{screenings_url}/{screening_id}")
        seat_id = screening_response.json()["seats"][0]["seat_id"]

        hold1 = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": [seat_id]},
            headers={"Authorization": registered_client_token},
        )
        await client.post(
            reservations_url,
            json={"hold_id": hold1.json()["hold_id"], "screening_id": screening_id},
            headers={"Authorization": registered_client_token},
        )

        response = await client.post(
            f"{screenings_url}/{screening_id}/seats/hold",
            json={"seat_ids": [seat_id]},
            headers={"Authorization": second_client_token},
        )

        assert response.status_code == 409
