import logging
from datetime import datetime

from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategorySlugAlreadyExistsException
from src.core.exceptions.domain_exceptions import CategorySlugAlreadyExistsException as DomainCategorySlugAlreadyExistsException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import CategoryCreateSchema, CategoryResponseSchema

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryCreateSchema) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = Category(
                title=data.title,
                description=data.description,
                slug=data.slug,
                is_published=data.is_published,
                created_at=datetime.now(),
            )

            try:
                self._repo.create(session=session, category=category)
            except CategorySlugAlreadyExistsException:
                error = DomainCategorySlugAlreadyExistsException(slug=data.slug)
                logger.error(error.get_detail())
                raise error

            return CategoryResponseSchema.model_validate(obj=category)
