from typing import Type

from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryUpdateSchema


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, category_id: int) -> Category | None:
        query = session.query(self._model).filter_by(id=category_id)
        return query.first()

    def get_all(self, session: Session) -> list[Category]:
        return session.query(self._model).all()

    def create(self, session: Session, category: Category) -> Category:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    def update(
        self, session: Session, category: Category, data: CategoryUpdateSchema
    ) -> Category:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(category, field, value)
        session.commit()
        session.refresh(category)
        return category

    def delete(self, session: Session, category: Category):
        session.delete(category)
        session.commit()
