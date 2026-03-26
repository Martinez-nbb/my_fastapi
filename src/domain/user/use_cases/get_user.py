import logging

from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserResponseSchema

logger = logging.getLogger(__name__)


class GetUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponseSchema:
        logger.debug('Получение пользователя по id: %s', user_id)
        with self._database.session() as session:
            try:
                user = self._repo.get(session=session, user_id=user_id)
            except UserNotFoundException as exc:
                logger.error(
                    'Пользователь не найден: user_id=%s, ошибка: %s',
                    user_id,
                    exc,
                )
                raise UserNotFoundByIdException(id=user_id)

        logger.debug('Пользователь успешно получен: %s', user_id)
        return UserResponseSchema.model_validate(obj=user)
