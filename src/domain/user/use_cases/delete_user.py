from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.core.logging import get_logger
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository

logger = get_logger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        logger.info(f"Удаление пользователя id={user_id}")
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, user_id=user_id)
                logger.info(f"Пользователь id={user_id} успешно удален")
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
