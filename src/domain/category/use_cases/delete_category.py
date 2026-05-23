import logging

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.category import CategoryRepository

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete(session=session, category_id=category_id)
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error
