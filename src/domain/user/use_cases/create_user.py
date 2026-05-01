from pydantic import SecretStr

from src.core.exceptions.database_exceptions import (
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import UserUsernameOrEmailIsNotUniqueException
from src.core.logging import get_logger
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserCreateSchema, UserResponseSchema
from src.resources.auth import get_password_hash

logger = get_logger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreateSchema) -> UserResponseSchema:
        logger.info(f"Создание пользователя: username={data.username}, email={data.email}")
        # Хешируем пароль перед сохранением
        hashed_password = get_password_hash(data.password.get_secret_value())
        data.password = SecretStr(hashed_password)
        
        with self._database.session() as session:
            try:
                user = self._repo.create(session=session, data=data)
                logger.info(f"Пользователь создан: id={user.id}, username={user.username}")
            except UserUsernameAlreadyExistsException:
                logger.warning(f"Попытка создания пользователя с существующим username: {data.username}")
                raise UserUsernameOrEmailIsNotUniqueException.from_username(
                    username=data.username
                )
            except UserEmailAlreadyExistsException:
                logger.warning(f"Попытка создания пользователя с существующим email: {data.email}")
                raise UserUsernameOrEmailIsNotUniqueException.from_email(
                    email=data.email
                )

            return UserResponseSchema.model_validate(obj=user)
