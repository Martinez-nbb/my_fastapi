from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    handle_database_exception,
)
from src.infrastructure.sqlite.models.post import Post
from src.schemas.posts import PostUpdateSchema


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, post_id: int) -> Post:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.location),
                joinedload(self._model.category),
            ).filter_by(id=post_id)

            post = query.first()

            if post is None:
                raise PostNotFoundException(f'Публикация с id={post_id} не найдена')

            return post
        except PostNotFoundException:
            raise
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'публикацией')

    def get_all(self, session: Session) -> list[Post]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.location),
                joinedload(self._model.category),
            )
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'получением списка публикаций')

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Post]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.location),
                joinedload(self._model.category),
            ).filter_by(author_id=author_id)
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'поиском публикаций по автору')

    def get_by_category(
        self,
        session: Session,
        category_id: int,
    ) -> list[Post]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.location),
                joinedload(self._model.category),
            ).filter_by(category_id=category_id)
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'поиском публикаций по категории')

    def get_by_location(
        self,
        session: Session,
        location_id: int,
    ) -> list[Post]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.location),
                joinedload(self._model.category),
            ).filter_by(location_id=location_id)
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'поиском публикаций по местоположению')

    def create(self, session: Session, post: Post) -> Post:
        try:
            session.add(post)
            session.flush()
            session.refresh(post)
            return post
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'созданием публикации')

    def update(
        self,
        session: Session,
        post: Post,
        data: PostUpdateSchema,
    ) -> Post:
        try:
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(post, field, value)
            session.flush()
            session.refresh(post)
            return post
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'обновлением публикации')

    def delete(self, session: Session, post: Post) -> None:
        try:
            session.delete(post)
            session.flush()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'удалением публикации')
