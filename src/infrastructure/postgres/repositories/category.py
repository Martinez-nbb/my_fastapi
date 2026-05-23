from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from src.infrastructure.postgres.models.category import Category as CategoryModel
from src.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema


class CategoryRepository:
    def __init__(self) -> None:
        self._model: Type[CategoryModel] = CategoryModel

    async def get(self, session: AsyncSession, category_id: int) -> CategoryModel:
        query = select(self._model).where(self._model.id == category_id)
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_by_slug(self, session: AsyncSession, slug: str) -> CategoryModel:
        query = select(self._model).where(self._model.slug == slug)
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_all(self, session: AsyncSession) -> list[CategoryModel]:
        query = select(self._model)
        result = await session.scalars(query)
        return list(result)

    async def create(self, session: AsyncSession, data: CategoryCreateSchema) -> CategoryModel:
        query = (
            insert(self._model)
            .values(
                title=data.title,
                description=data.description,
                slug=data.slug,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        category = await session.scalar(query)

        return category

    async def update(
        self,
        session: AsyncSession,
        category_id: int,
        data: CategoryUpdateSchema,
    ) -> CategoryModel:
        category = await self.get(session=session, category_id=category_id)

        update_data = data.model_dump(exclude_none=True)

        query = (
            update(self._model)
            .where(self._model.id == category_id)
            .values(**update_data)
            .returning(self._model)
        )
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    async def delete(self, session: AsyncSession, category_id: int) -> None:
        query = delete(self._model).where(self._model.id == category_id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise CategoryNotFoundException()
