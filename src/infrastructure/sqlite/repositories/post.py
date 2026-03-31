from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from src.core.exceptions.database_exceptions import PostNotFoundException
from src.infrastructure.sqlite.models.post import Post
from src.schemas.posts import PostUpdateSchema


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, post_id: int) -> Post:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).where(self._model.id == post_id)

        post = session.scalar(query)
        if not post:
            raise PostNotFoundException()
        return post

    def get_all(self, session: Session) -> list[Post]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        )
        return list(session.scalars(query))

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Post]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).where(self._model.author_id == author_id)
        return list(session.scalars(query))

    def get_by_category(
        self,
        session: Session,
        category_id: int,
    ) -> list[Post]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).where(self._model.category_id == category_id)
        return list(session.scalars(query))

    def get_by_location(
        self,
        session: Session,
        location_id: int,
    ) -> list[Post]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).where(self._model.location_id == location_id)
        return list(session.scalars(query))

    def create(self, session: Session, post: Post) -> Post:
        query = insert(self._model).values(
            title=post.title,
            text=post.text,
            pub_date=post.pub_date,
            author_id=post.author_id,
            location_id=post.location_id,
            category_id=post.category_id,
            is_published=post.is_published,
            created_at=post.created_at,
        ).returning(self._model)

        try:
            created_post = session.scalar(query)
            session.refresh(created_post)
            return created_post
        except IntegrityError:
            raise PostNotFoundException()

    def update(
        self,
        session: Session,
        post: Post,
        data: PostUpdateSchema,
    ) -> Post:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(post, field, value)
        session.flush()
        session.refresh(post)
        return post

    def delete(self, session: Session, post: Post) -> None:
        session.delete(post)
        session.flush()
