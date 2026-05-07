import pytest
from datetime import datetime

from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.core.exceptions.database_exceptions import UserUsernameAlreadyExistsException
from src.schemas.users import UserCreateSchema
from pydantic import SecretStr

from tests.mocks import CallRecorder, FakeRow


class TestCreateUserUseCase:
    @pytest.mark.asyncio
    async def test_creates_user_successfully(
        self, create_user_use_case: CreateUserUseCase
    ) -> None:
        db_user: FakeRow = FakeRow(
            id=1,
            username="new_user",
            password="hashed_password",
            first_name="New",
            last_name="User",
            email="new@test.com",
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )
        create_user_use_case._repo.create = CallRecorder(return_value=db_user)

        data = UserCreateSchema(
            username="new_user",
            email="new@test.com",
            password=SecretStr("password123"),
            first_name="New",
            last_name="User",
        )

        result = await create_user_use_case.execute(data=data)

        assert result.username == "new_user"
        create_user_use_case._repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_when_username_exists(
        self, create_user_use_case: CreateUserUseCase
    ) -> None:
        create_user_use_case._repo.create = CallRecorder(
            side_effect=UserUsernameAlreadyExistsException()
        )

        data = UserCreateSchema(
            username="existing",
            email="new@test.com",
            password=SecretStr("password123"),
            first_name="New",
            last_name="User",
        )

        with pytest.raises(Exception):
            await create_user_use_case.execute(data=data)