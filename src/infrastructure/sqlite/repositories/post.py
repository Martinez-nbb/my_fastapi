from typing import Type

from sqlalchemy.orm import Session, joinedload

from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.models.post import Post
from src.schemas.posts import PostUpdateSchema


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, post_id: int) -> Post:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).filter_by(id=post_id)

        post = query.first()

        if post is None:
            raise PostNotFoundByIdException(id=post_id)

        return post

    def get_all(self, session: Session) -> list[Post]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        )
        return query.all()

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Post]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).filter_by(author_id=author_id)
        return query.all()

    def get_by_category(
        self,
        session: Session,
        category_id: int,
    ) -> list[Post]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).filter_by(category_id=category_id)
        return query.all()

    def get_by_location(
        self,
        session: Session,
        location_id: int,
    ) -> list[Post]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.location),
            joinedload(self._model.category),
        ).filter_by(location_id=location_id)
        return query.all()

    def create(self, session: Session, post: Post) -> Post:
        session.add(post)
        session.flush()
        session.refresh(post)
        return post

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
