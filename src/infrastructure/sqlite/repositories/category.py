from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    handle_database_exception,
)
from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryUpdateSchema


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, category_id: int) -> Category:
        try:
            query = session.query(self._model).filter_by(id=category_id)
            category = query.first()
            if category is None:
                raise CategoryNotFoundException(f'Категория с id={category_id} не найдена')
            return category
        except CategoryNotFoundException:
            raise
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'категорией')

    def get_by_slug(
        self,
        session: Session,
        slug: str,
    ) -> Category | None:
        try:
            query = session.query(self._model).filter_by(slug=slug)
            return query.first()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'поиском категории по slug')

    def get_all(self, session: Session) -> list[Category]:
        try:
            return session.query(self._model).all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'получением списка категорий')

    def create(self, session: Session, category: Category) -> Category:
        try:
            session.add(category)
            session.flush()
            session.refresh(category)
            return category
        except SQLAlchemyError as exc:
            if 'slug' in str(exc.orig).lower():
                raise CategorySlugAlreadyExistsException(
                    f'Категория со slug "{category.slug}" уже существует'
                )
            raise handle_database_exception(exc, 'созданием категории')

    def update(
        self,
        session: Session,
        category: Category,
        data: CategoryUpdateSchema,
    ) -> Category:
        try:
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(category, field, value)
            session.flush()
            session.refresh(category)
            return category
        except SQLAlchemyError as exc:
            if 'slug' in str(exc.orig).lower():
                raise CategorySlugAlreadyExistsException(
                    f'Категория со slug "{category.slug}" уже существует'
                )
            raise handle_database_exception(exc, 'обновлением категории')

    def delete(self, session: Session, category: Category) -> None:
        try:
            session.delete(category)
            session.flush()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'удалением категории')
