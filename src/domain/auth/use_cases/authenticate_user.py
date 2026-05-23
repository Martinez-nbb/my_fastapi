import logging

from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.user import UserRepository
from src.schemas.users import UserResponseSchema
from src.resources.auth import async_verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import (
    InvalidCredentialsException,
    UserNotFoundByUsernameException,
)


logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        username: str,
        password: str,
    ) -> UserResponseSchema:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_by_username(session=session, username=username)
                hashed_password = user.password
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'date_joined': user.date_joined,
                }
        except UserNotFoundException:
            error = UserNotFoundByUsernameException(username=username)
            logger.error(error.get_detail())
            raise error

        if not await async_verify_password(
            plain_password=password, hashed_password=hashed_password
        ):
            logger.error(f"Wrong password for user: {username}")
            raise InvalidCredentialsException()

        return UserResponseSchema(**user_data)
