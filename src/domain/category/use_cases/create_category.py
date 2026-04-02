import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.domain_exceptions import CategorySlugAlreadyExistsException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import CategoryCreateSchema, CategoryResponseSchema

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryCreateSchema) -> CategoryResponseSchema:
        with self._database.session() as session:
            try:
                category = self._repo.create(session=session, data=data)
            except IntegrityError:
                error = CategorySlugAlreadyExistsException(slug=data.slug)
                logger.error(error.get_detail())
                raise error

            return CategoryResponseSchema.model_validate(obj=category)
