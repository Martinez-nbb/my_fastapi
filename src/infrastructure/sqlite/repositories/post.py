from datetime import datetime
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
    LocationNotFoundException,
    CategoryNotFoundException,
)
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.infrastructure.sqlite.models.user import User as UserModel
from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.posts import PostCreateSchema, PostUpdateSchema


class PostRepository:
    def __init__(self) -> None:
        self._model: Type[PostModel] = PostModel
        self._author_model: Type[UserModel] = UserModel
        self._location_model: Type[LocationModel] = LocationModel
        self._category_model: Type[CategoryModel] = CategoryModel

    def get(self, session: Session, post_id: int) -> PostModel:
        query = select(self._model).where(self._model.id == post_id)
        post = session.scalar(query)

        if not post:
            raise PostNotFoundException()

        return post

    def get_all(self, session: Session) -> list[PostModel]:
        query = select(self._model)
        return list(session.scalars(query))

    def get_by_author(self, session: Session, author_id: int) -> list[PostModel]:
        query = select(self._model).where(self._model.author_id == author_id)
        return list(session.scalars(query))

    def get_by_category(
        self,
        session: Session,
        category_id: int,
    ) -> list[PostModel]:
        query = select(self._model).where(self._model.category_id == category_id)
        return list(session.scalars(query))

    def get_by_location(
        self,
        session: Session,
        location_id: int,
    ) -> list[PostModel]:
        query = select(self._model).where(self._model.location_id == location_id)
        return list(session.scalars(query))

    def create(self, session: Session, data: PostCreateSchema) -> PostModel:
        author = session.get(self._author_model, data.author_id)
        if not author:
            raise UserNotFoundException()

        if data.location_id is not None:
            location = session.get(self._location_model, data.location_id)
            if not location:
                raise LocationNotFoundException()

        if data.category_id is not None:
            category = session.get(self._category_model, data.category_id)
            if not category:
                raise CategoryNotFoundException()

        query = (
            insert(self._model)
            .values(
                title=data.title,
                text=data.text,
                pub_date=data.pub_date,
                author_id=data.author_id,
                location_id=data.location_id,
                category_id=data.category_id,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def update(
        self,
        session: Session,
        post_id: int,
        data: PostUpdateSchema,
    ) -> PostModel:
        post = self.get(session=session, post_id=post_id)

        update_data = data.model_dump(exclude_none=True)

        if 'author_id' in update_data and update_data['author_id'] != post.author_id:
            author = session.get(self._author_model, update_data['author_id'])
            if not author:
                raise UserNotFoundException()

        if (
            'location_id' in update_data
            and update_data['location_id'] is not None
            and update_data['location_id'] != post.location_id
        ):
            location = session.get(self._location_model, update_data['location_id'])
            if not location:
                raise LocationNotFoundException()

        if (
            'category_id' in update_data
            and update_data['category_id'] is not None
            and update_data['category_id'] != post.category_id
        ):
            category = session.get(self._category_model, update_data['category_id'])
            if not category:
                raise CategoryNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(**update_data)
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def delete(self, session: Session, post_id: int) -> None:
        query = delete(self._model).where(self._model.id == post_id)
        result = cast(CursorResult, session.execute(query))

        if not result.rowcount:
            raise PostNotFoundException()
