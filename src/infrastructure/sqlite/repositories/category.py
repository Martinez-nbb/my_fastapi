from datetime import datetime
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema


class CategoryRepository:
    def __init__(self) -> None:
        self._model: Type[CategoryModel] = CategoryModel

    def get(self, session: Session, category_id: int) -> CategoryModel:
        query = select(self._model).where(self._model.id == category_id)
        category = session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    def get_by_slug(self, session: Session, slug: str) -> CategoryModel:
        query = select(self._model).where(self._model.slug == slug)
        category = session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    def get_all(self, session: Session) -> list[CategoryModel]:
        query = select(self._model)
        return list(session.scalars(query))

    def create(self, session: Session, data: CategoryCreateSchema) -> CategoryModel:
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
        category = session.scalar(query)

        return category

    def update(
        self,
        session: Session,
        category_id: int,
        data: CategoryUpdateSchema,
    ) -> CategoryModel:
        category = self.get(session=session, category_id=category_id)

        update_data = data.model_dump(exclude_none=True)

        query = (
            update(self._model)
            .where(self._model.id == category_id)
            .values(**update_data)
            .returning(self._model)
        )
        category = session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    def delete(self, session: Session, category_id: int) -> None:
        query = delete(self._model).where(self._model.id == category_id)
        result = cast(CursorResult, session.execute(query))

        if not result.rowcount:
            raise CategoryNotFoundException()
