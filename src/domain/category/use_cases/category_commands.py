import logging
from datetime import datetime

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        data: CategoryCreateSchema,
    ) -> CategoryResponseSchema:
        logger.debug('Создание категории: slug=%s', data.slug)
        with self._database.session() as session:
            existing = self._repo.get_by_slug(
                session=session,
                slug=data.slug,
            )
            if existing is not None:
                logger.warning(
                    'Попытка создания существующей категории: slug=%s',
                    data.slug,
                )
                raise CategoryNotFoundByIdException(id=existing.id)

            category = Category(
                title=data.title,
                description=data.description,
                slug=data.slug,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            self._repo.create(session=session, category=category)

        logger.info('Категория успешно создана: slug=%s', data.slug)
        return CategoryResponseSchema.model_validate(obj=category)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        category_id: int,
        data: CategoryUpdateSchema,
    ) -> CategoryResponseSchema:
        logger.debug('Обновление категории: category_id=%s', category_id)
        with self._database.session() as session:
            try:
                category = self._repo.get(
                    session=session,
                    category_id=category_id,
                )
            except CategoryNotFoundException as exc:
                logger.error(
                    'Категория не найдена для обновления: category_id=%s, ошибка: %s',
                    category_id,
                    exc,
                )
                raise CategoryNotFoundByIdException(id=category_id)

            self._repo.update(
                session=session,
                category=category,
                data=data,
            )

        logger.info('Категория успешно обновлена: %s', category_id)
        return CategoryResponseSchema.model_validate(obj=category)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        logger.debug('Удаление категории: category_id=%s', category_id)
        with self._database.session() as session:
            try:
                category = self._repo.get(
                    session=session,
                    category_id=category_id,
                )
            except CategoryNotFoundException as exc:
                logger.error(
                    'Категория не найдена для удаления: category_id=%s, ошибка: %s',
                    category_id,
                    exc,
                )
                raise CategoryNotFoundByIdException(id=category_id)

            self._repo.delete(session=session, category=category)

        logger.info('Категория успешно удалена: %s', category_id)
