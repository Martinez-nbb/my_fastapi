import pytest

from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.core.config import settings


class TestCreateAccessTokenUseCase:
    @pytest.mark.asyncio
    async def test_creates_token_with_username(self):
        """Тест создания токена для пользователя."""
        use_case = CreateAccessTokenUseCase()

        token = await use_case.execute(username="test_user")

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    @pytest.mark.asyncio
    async def test_token_contains_username_in_payload(self):
        """Тест проверки содержимого токена."""
        from jose import jwt

        use_case = CreateAccessTokenUseCase()
        username = "test_user"

        token = await use_case.execute(username=username)

        payload = jwt.decode(
            token,
            settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM]
        )

        assert payload["sub"] == username

    @pytest.mark.asyncio
    async def test_token_has_expiration(self):
        """Тест наличия срока действия токена."""
        from jose import jwt

        use_case = CreateAccessTokenUseCase()

        token = await use_case.execute(username="test_user")

        payload = jwt.decode(
            token,
            settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM]
        )

        assert "exp" in payload
        assert payload["exp"] > payload["iat"]

    @pytest.mark.asyncio
    async def test_different_tokens_for_different_usernames(self):
        """Тест генерации разных токенов для разных пользователей."""
        use_case = CreateAccessTokenUseCase()

        token1 = await use_case.execute(username="user1")
        token2 = await use_case.execute(username="user2")

        assert token1 != token2