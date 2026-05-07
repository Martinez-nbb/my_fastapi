import pytest
from datetime import datetime

from pydantic import ValidationError

from src.schemas.users import (
    UserResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from pydantic import SecretStr


class TestUserResponseSchema:
    def test_create_user_response_schema(self):
        """Тест создания схемы ответа пользователя."""
        data = {
            "id": 1,
            "username": "test_user",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@test.com",
            "is_active": True,
            "is_superuser": False,
            "is_staff": False,
            "date_joined": datetime.now(),
        }

        schema = UserResponseSchema(**data)

        assert schema.username == "test_user"
        assert schema.email == "test@test.com"
        assert schema.is_active is True

    def test_user_schema_with_all_flags(self):
        """Тест схемы со всеми флагами."""
        data = {
            "id": 1,
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@test.com",
            "is_active": True,
            "is_superuser": True,
            "is_staff": True,
            "date_joined": datetime.now(),
        }

        schema = UserResponseSchema(**data)

        assert schema.is_superuser is True
        assert schema.is_staff is True

    def test_user_schema_fields_types(self):
        """Тест типов полей схемы."""
        now = datetime.now()
        data = {
            "id": 1,
            "username": "user",
            "first_name": "First",
            "last_name": "Last",
            "email": "email@test.com",
            "is_active": True,
            "is_superuser": False,
            "is_staff": False,
            "date_joined": now,
        }

        schema = UserResponseSchema(**data)

        assert isinstance(schema.id, int)
        assert isinstance(schema.username, str)
        assert isinstance(schema.is_active, bool)


class TestUserCreateSchema:
    def test_create_user_with_valid_data(self):
        """Тест создания пользователя с валидными данными."""
        data = {
            "username": "new_user",
            "email": "new@test.com",
            "password": SecretStr("password123"),
            "first_name": "New",
            "last_name": "User",
        }

        schema = UserCreateSchema(**data)

        assert schema.username == "new_user"
        assert schema.email == "new@test.com"
        assert schema.first_name == "New"

    def test_create_user_without_optional_fields(self):
        """Тест создания пользователя без необязательных полей."""
        data = {
            "username": "minimal_user",
            "email": "minimal@test.com",
            "password": SecretStr("password123"),
        }

        schema = UserCreateSchema(**data)

        assert schema.username == "minimal_user"
        assert schema.first_name is None
        assert schema.last_name is None

    def test_create_user_with_invalid_email(self):
        """Тест ошибки при невалидном email."""
        data = {
            "username": "user",
            "email": "not-an-email",
            "password": SecretStr("password123"),
        }

        with pytest.raises(ValidationError):
            UserCreateSchema(**data)

    def test_create_user_with_short_password(self):
        """Тест ошибки при коротком пароле."""
        data = {
            "username": "user",
            "email": "test@test.com",
            "password": SecretStr("123"),
        }

        with pytest.raises(ValidationError):
            UserCreateSchema(**data)


class TestUserUpdateSchema:
    def test_create_update_schema_with_all_fields(self):
        """Тест схемы обновления со всеми полями."""
        data = {
            "first_name": "UpdatedName",
            "last_name": "UpdatedLastName",
            "email": "updated@test.com",
        }

        schema = UserUpdateSchema(**data)

        assert schema.first_name == "UpdatedName"
        assert schema.last_name == "UpdatedLastName"
        assert schema.email == "updated@test.com"

    def test_create_update_schema_partial(self):
        """Тест частичного обновления."""
        schema = UserUpdateSchema(first_name="NewName")

        assert schema.first_name == "NewName"
        assert schema.last_name is None
        assert schema.email is None