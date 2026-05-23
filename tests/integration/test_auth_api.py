import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from tests.mocks import FakeRow


class TestAuthAPI:
    """Integration tests for authentication endpoints."""

    @pytest.mark.asyncio
    async def test_register_success(self, async_client, valid_user_payload, mock_repo):
        """Тест успешной регистрации пользователя через API."""
        mock_repo_instance = AsyncMock()
        mock_repo["user"].return_value = mock_repo_instance
        
        db_user = FakeRow(
            id=1,
            username=valid_user_payload["username"],
            email=valid_user_payload["email"],
            first_name=valid_user_payload["first_name"],
            last_name=valid_user_payload["last_name"],
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )
        mock_repo_instance.create.return_value = db_user

        response = await async_client.post("/users/", json=valid_user_payload)

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == valid_user_payload["username"]
        assert data["email"] == valid_user_payload["email"]

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, async_client, valid_user_payload, mock_repo):
        """Тест регистрации с существующим именем пользователя."""
        from src.core.exceptions.domain_exceptions import UserUsernameOrEmailIsNotUniqueException
        
        mock_repo_instance = AsyncMock()
        mock_repo["user"].return_value = mock_repo_instance
        mock_repo_instance.create.side_effect = UserUsernameOrEmailIsNotUniqueException.from_username("testuser")

        response = await async_client.post("/users/", json=valid_user_payload)

        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_login_success(self, async_client, valid_user_payload, mock_repo):
        """Тест успешного входа в систему."""
        from src.resources.auth import get_password_hash

        mock_repo_instance = AsyncMock()
        mock_repo["auth"].return_value = mock_repo_instance

        hashed = get_password_hash(valid_user_payload["password"])
        db_user = FakeRow(
            id=1,
            username=valid_user_payload["username"],
            password=hashed,
            email=valid_user_payload["email"],
            first_name=valid_user_payload["first_name"],
            last_name=valid_user_payload["last_name"],
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )
        mock_repo_instance.get_by_username.return_value = db_user

        with patch(
            "src.domain.auth.use_cases.create_refresh_token.CreateRefreshTokenUseCase.execute",
            return_value="fake_refresh_token",
        ):
            login_data = {
                "username": valid_user_payload["username"],
                "password": valid_user_payload["password"],
            }
            response = await async_client.post("/auth/token", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["refresh_token"] == "fake_refresh_token"
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, async_client, valid_user_payload, mock_repo):
        """Тест входа с неверным паролем."""
        from src.resources.auth import get_password_hash
        
        mock_repo_instance = AsyncMock()
        mock_repo["auth"].return_value = mock_repo_instance
        
        hashed = get_password_hash("real_password")
        db_user = FakeRow(
            id=1,
            username=valid_user_payload["username"],
            password=hashed,
            email=valid_user_payload["email"],
            first_name=valid_user_payload["first_name"],
            last_name=valid_user_payload["last_name"],
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )
        mock_repo_instance.get_by_username.return_value = db_user

        login_data = {
            "username": valid_user_payload["username"],
            "password": "wrong_password"
        }
        response = await async_client.post("/auth/token", data=login_data)

        assert response.status_code == 401
