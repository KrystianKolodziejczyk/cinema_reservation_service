import pytest

pytestmark = pytest.mark.anyio


class TestRegisterEndpoint:
    async def test_register_success(self, client, register_url, user_payload):
        response = await client.post(register_url, json=user_payload)

        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    async def test_register_duplicate_email(self, client, register_url, user_payload):
        await client.post(register_url, json=user_payload)
        response = await client.post(register_url, json=user_payload)

        assert response.status_code == 409

    async def test_register_mismatched_passwords(
        self, client, register_url, user_payload
    ):
        payload = {**user_payload, "password_repeat": "completely_different"}
        response = await client.post(register_url, json=payload)

        assert response.status_code == 409


class TestLoginEndpoint:
    async def test_login_success(
        self, client, login_url, registered_user, user_payload
    ):
        response = await client.post(
            login_url,
            json={
                "email": user_payload["email"],
                "password": user_payload["password"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    async def test_login_wrong_password(
        self, client, login_url, registered_user, user_payload
    ):
        response = await client.post(
            login_url,
            json={
                "email": user_payload["email"],
                "password": "wrong_password_here",
            },
        )

        assert response.status_code == 409

    async def test_login_user_not_found(self, client, login_url):
        response = await client.post(
            login_url,
            json={
                "email": "nonexistent@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 404


class TestLogoutEndpoint:
    async def test_logout_success(self, client, logout_url, registered_user):
        response = await client.post(
            logout_url, json={"refresh_token": registered_user["refresh_token"]}
        )

        assert response.status_code == 204

    async def test_logout_invalid_token(self, client, logout_url):
        response = await client.post(
            logout_url, json={"refresh_token": "invalid.token.value"}
        )

        assert response.status_code == 409


class TestRefreshEndpoint:
    async def test_refresh_success(self, client, refresh_url, registered_user):
        response = await client.post(
            refresh_url, json={"refresh_token": registered_user["refresh_token"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    async def test_refresh_token_reuse(self, client, refresh_url, registered_user):
        old_token = registered_user["refresh_token"]
        await client.post(refresh_url, json={"refresh_token": old_token})

        response = await client.post(refresh_url, json={"refresh_token": old_token})

        assert response.status_code == 404
