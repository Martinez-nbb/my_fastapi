import logging
import bcrypt

from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreateSchema) -> UserResponseSchema:
        logger.debug('Создание пользователя: %s', data.username)
        with self._database.session() as session:
            existing = self._repo.get_by_username(
                session=session,
                username=data.username,
            )
            if existing is not None:
                logger.warning(
                    'Попытка создания существующего пользователя: %s',
                    data.username,
                )
                raise UserNotFoundByUsernameException(username=data.username)

            user = User(
                username=data.username,
                password=hash_password(data.password.get_secret_value()),
                email=data.email or '',
                first_name=data.first_name,
                last_name=data.last_name,
                is_active=True,
            )
            self._repo.create(session=session, user=user)

        logger.info('Пользователь успешно создан: %s', data.username)
        return UserResponseSchema.model_validate(obj=user)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        user_id: int,
        data: UserUpdateSchema,
    ) -> UserResponseSchema:
        logger.debug('Обновление пользователя: user_id=%s', user_id)
        with self._database.session() as session:
            try:
                user = self._repo.get(
                    session=session,
                    user_id=user_id,
                )
            except UserNotFoundException as exc:
                logger.error(
                    'Пользователь не найден для обновления: user_id=%s, ошибка: %s',
                    user_id,
                    exc,
                )
                raise UserNotFoundByIdException(id=user_id)

            self._repo.update(
                session=session,
                user=user,
                data=data,
            )

        logger.info('Пользователь успешно обновлён: %s', user_id)
        return UserResponseSchema.model_validate(obj=user)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        logger.debug('Удаление пользователя: user_id=%s', user_id)
        with self._database.session() as session:
            try:
                user = self._repo.get(
                    session=session,
                    user_id=user_id,
                )
            except UserNotFoundException as exc:
                logger.error(
                    'Пользователь не найден для удаления: user_id=%s, ошибка: %s',
                    user_id,
                    exc,
                )
                raise UserNotFoundByIdException(id=user_id)

            self._repo.delete(session=session, user=user)

        logger.info('Пользователь успешно удалён: %s', user_id)
