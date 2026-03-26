import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserResponseSchema

logger = logging.getLogger(__name__)


class GetUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[UserResponseSchema]:
        logger.debug('Получение списка всех пользователей')
        with self._database.session() as session:
            users = self._repo.get_all(session=session)
        logger.debug('Получено пользователей: %s', len(users))
        return [
            UserResponseSchema.model_validate(obj=user)
            for user in users
        ]
