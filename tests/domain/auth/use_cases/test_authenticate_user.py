import pytest

from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.resources.auth import get_password_hash, verify_password

from tests.mocks import CallRecorder, FakeRow


class TestAuthenticateUserUseCase:
    @pytest.mark.asyncio
    async def test_returns_user_when_credentials_are_valid(self):
        """Тест успешной аутентификации с правильными данными."""
        uc = AuthenticateUserUseCase()
        uc._repo = FakeRow()

        hashed = get_password_hash("correct-password")
        db_user = FakeRow(
            id=1,
            username="test_user",
            password=hashed,
            first_name="Test",
            last_name="User",
            email="test@test.com",
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined="2024-01-01",
        )
        uc._repo.get_by_username = CallRecorder(return_value=db_user)

        result = await uc.execute(username="test_user", password="correct-password")

        assert result.username == "test_user"
        assert result.email == "test@test.com"
        assert result.is_active is True

    @pytest.mark.asyncio
    async def test_raises_when_user_not_found(self):
        """Тест ошибки при отсутствии пользователя."""
        uc = AuthenticateUserUseCase()
        uc._repo = FakeRow()
        uc._repo.get_by_username = CallRecorder(side_effect=Exception("User not found"))

        with pytest.raises(Exception, match="User not found"):
            await uc.execute(username="missing", password="x")

    @pytest.mark.asyncio
    async def test_raises_when_password_is_wrong(self):
        """Тест ошибки при неверном пароле."""
        uc = AuthenticateUserUseCase()
        uc._repo = FakeRow()

        hashed = get_password_hash("the-real-password")
        db_user = FakeRow(
            id=1,
            username="test_user",
            password=hashed,
            first_name="Test",
            last_name="User",
            email="test@test.com",
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined="2024-01-01",
        )
        uc._repo.get_by_username = CallRecorder(return_value=db_user)

        with pytest.raises(ValueError, match="Неверный пароль"):
            await uc.execute(username="test_user", password="wrong-password")

    @pytest.mark.asyncio
    async def test_returns_user_with_all_fields(self):
        """Тест проверки всех полей пользователя."""
        uc = AuthenticateUserUseCase()
        uc._repo = FakeRow()

        hashed = get_password_hash("password123")
        db_user = FakeRow(
            id=42,
            username="admin_user",
            password=hashed,
            first_name="Admin",
            last_name="Super",
            email="admin@example.com",
            is_active=True,
            is_superuser=True,
            is_staff=True,
            date_joined="2024-06-15",
        )
        uc._repo.get_by_username = CallRecorder(return_value=db_user)

        result = await uc.execute(username="admin_user", password="password123")

        assert result.id == 42
        assert result.username == "admin_user"
        assert result.first_name == "Admin"
        assert result.last_name == "Super"
        assert result.email == "admin@example.com"
        assert result.is_active is True
        assert result.is_superuser is True
        assert result.is_staff is True