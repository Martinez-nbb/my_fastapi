from datetime import datetime

from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)


class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.get(
                session=session,
                category_id=category_id,
            )

            if category is None:
                raise HTTPException(
                    status_code=404,
                    detail=f'Категория с id={category_id} не найдена',
                )

            return CategoryResponseSchema.model_validate(obj=category)


class GetCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> list[CategoryResponseSchema]:
        with self._database.session() as session:
            categories = self._repo.get_all(session=session)
            return [
                CategoryResponseSchema.model_validate(obj=cat)
                for cat in categories
            ]


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
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f'Категория со slug "{data.slug}" уже существует',
                )

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
            category = self._repo.get(
                session=session,
                category_id=category_id,
            )

            if category is None:
                raise HTTPException(
                    status_code=404,
                    detail=f'Категория с id={category_id} не найдена',
                )

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
            category = self._repo.get(
                session=session,
                category_id=category_id,
            )

            if category is None:
                raise HTTPException(
                    status_code=404,
                    detail=f'Категория с id={category_id} не найдена',
                )

            self._repo.delete(session=session, category=category)
