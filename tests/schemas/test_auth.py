import pytest
from datetime import datetime, timedelta

from src.schemas.auth import Token, TokenData


class TestTokenSchema:
    def test_create_token_schema(self):
        """Тест создания токена."""
        token = Token(access_token="test_token_123", token_type="bearer")

        assert token.access_token == "test_token_123"
        assert token.token_type == "bearer"

    def test_token_default_token_type(self):
        """Тест значения по умолчанию для token_type."""
        token = Token(access_token="token123")

        assert token.token_type == "bearer"

    def test_token_schema_fields(self):
        """Тест полей токена."""
        token = Token(access_token="abc123", token_type="bearer")

        assert hasattr(token, 'access_token')
        assert hasattr(token, 'token_type')
        assert isinstance(token.access_token, str)


class TestTokenDataSchema:
    def test_create_token_data(self):
        """Тест создания данных токена."""
        data = TokenData(username="test_user")

        assert data.username == "test_user"

    def test_token_data_with_expires_delta(self):
        """Тест данных токена с временем жизни."""
        exp = 1715089600

        data = TokenData(username="user", exp=exp)

        assert data.username == "user"
        assert data.exp == exp