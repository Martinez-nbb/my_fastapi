import logging

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        try:
            with self._database.session() as session:
                category = self._repo.get(session=session, category_id=category_id)
                self._repo.delete(session=session, category=category)
        except CategoryNotFoundException:
            error = CategoryNotFoundByIdException(id=category_id)
            logger.error(error.get_detail())
            raise error
