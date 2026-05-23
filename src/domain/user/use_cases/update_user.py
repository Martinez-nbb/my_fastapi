from sqlalchemy.exc import IntegrityError

from src.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserUsernameOrEmailIsNotUniqueException,
)
from src.core.logging import get_logger
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.user import UserRepository
from src.schemas.users import UserUpdateSchema, UserResponseSchema

logger = get_logger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        user_id: int,
        data: UserUpdateSchema,
    ) -> UserResponseSchema:
        logger.info(f"Обновление пользователя id={user_id}, данные: {data.model_dump(exclude_unset=True)}")
        async with self._database.session() as session:
            try:
                user = await self._repo.update(
                    session=session,
                    user_id=user_id,
                    data=data,
                )
                logger.info(f"Пользователь id={user_id} успешно обновлен")
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
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
            except UserEmailAlreadyExistsException:
                error = UserUsernameOrEmailIsNotUniqueException.from_email(email=data.email)
                logger.error(error.get_detail())
                raise error
            except UserUsernameAlreadyExistsException:
                error = UserUsernameOrEmailIsNotUniqueException.from_username(
                    username=data.username
                )
                logger.error(error.get_detail())
                raise error
            except IntegrityError as e:
                logger.error(f"IntegrityError при обновлении пользователя: {e}")
                raise UserUsernameOrEmailIsNotUniqueException(
                    detail="Ошибка целостности данных при обновлении пользователя"
                )

        return UserResponseSchema(**user_data)
