from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.core.logging import get_logger
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
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
        with self._database.session() as session:
            try:
                user = self._repo.update(
                    session=session,
                    user_id=user_id,
                    data=data,
                )
                logger.info(f"Пользователь id={user_id} успешно обновлен")
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error

            return UserResponseSchema.model_validate(obj=user)
