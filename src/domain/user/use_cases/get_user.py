import logging

from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.user import UserRepository
from src.schemas.users import UserResponseSchema

logger = logging.getLogger(__name__)


class GetUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponseSchema:
        async with self._database.session() as session:
            try:
                user = await self._repo.get(session=session, user_id=user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error

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

        return UserResponseSchema(**user_data)
