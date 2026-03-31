from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
)
from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryUpdateSchema


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, category_id: int) -> Category:
        query = select(self._model).where(self._model.id == category_id)
        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException()
        return category

    def get_by_slug(
        self,
        session: Session,
        slug: str,
    ) -> Category:
        query = select(self._model).where(self._model.slug == slug)
        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException()
        return category

    def get_all(self, session: Session) -> list[Category]:
        query = select(self._model)
        return list(session.scalars(query))

    def create(self, session: Session, category: Category) -> Category:
        query = insert(self._model).values(
            title=category.title,
            description=category.description,
            slug=category.slug,
            is_published=category.is_published,
            created_at=category.created_at,
        ).returning(self._model)

        try:
            created_category = session.scalar(query)
            session.refresh(created_category)
            return created_category
        except IntegrityError:
            raise CategorySlugAlreadyExistsException()

    def update(
        self,
        session: Session,
        category: Category,
        data: CategoryUpdateSchema,
    ) -> Category:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(category, field, value)
        session.flush()
        session.refresh(category)
        return category

    def delete(self, session: Session, category: Category) -> None:
        session.delete(category)
        session.flush()
