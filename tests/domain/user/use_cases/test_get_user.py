import pytest
from datetime import datetime

from src.domain.user.use_cases.get_user import GetUserUseCase
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException

from tests.mocks import CallRecorder, FakeRow


class TestGetUserUseCase:
    @pytest.mark.asyncio
    async def test_returns_user_by_id(self, get_user_use_case: GetUserUseCase) -> None:
        db_user: FakeRow = FakeRow(
            id=1,
            username="test_user",
            password="hashed",
            first_name="Test",
            last_name="User",
            email="test@test.com",
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
        )
        get_user_use_case._repo.get = CallRecorder(return_value=db_user)

        result = await get_user_use_case.execute(user_id=1)

        assert result.username == "test_user"
        get_user_use_case._repo.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_when_user_not_found(self, get_user_use_case: GetUserUseCase) -> None:
        get_user_use_case._repo.get = CallRecorder(
            side_effect=UserNotFoundException()
        )

        with pytest.raises(UserNotFoundByIdException):
            await get_user_use_case.execute(user_id=999)