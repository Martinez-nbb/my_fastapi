import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserResponseSchema
from src.resources.auth import verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException


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
            with self._database.session() as session:
                user = self._repo.get_by_username(session=session, username=username)
                # Получаем пароль внутри сессии
                hashed_password = user.password
                # Создаем схему внутри сессии, чтобы загрузить все атрибуты
                user_schema = UserResponseSchema.model_validate(user)
        except UserNotFoundException:
            logger.error(f"User not found: {username}")
            raise

        if not verify_password(
            plain_password=password, hashed_password=hashed_password
        ):
            logger.error(f"Wrong password for user: {username}")
            raise ValueError("Неверный пароль")

        return user_schema
