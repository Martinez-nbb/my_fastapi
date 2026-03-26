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


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        data: CategoryCreateSchema,
    ) -> CategoryResponseSchema:
        with self._database.session() as session:
            existing = self._repo.get_by_slug(
                session=session,
                slug=data.slug,
            )
            if existing is not None:
                raise CategoryNotFoundByIdException(id=existing.id)

            category = Category(
                title=data.title,
                description=data.description,
                slug=data.slug,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            self._repo.create(session=session, category=category)

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
        with self._database.session() as session:
            try:
                category = self._repo.get(
                    session=session,
                    category_id=category_id,
                )
            except CategoryNotFoundException as exc:
                raise CategoryNotFoundByIdException(id=category_id)

            self._repo.update(
                session=session,
                category=category,
                data=data,
            )

        return CategoryResponseSchema.model_validate(obj=category)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            try:
                category = self._repo.get(
                    session=session,
                    category_id=category_id,
                )
            except CategoryNotFoundException as exc:
                raise CategoryNotFoundByIdException(id=category_id)

            self._repo.delete(session=session, category=category)
