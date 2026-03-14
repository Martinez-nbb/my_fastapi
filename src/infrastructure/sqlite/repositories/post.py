from typing import Type

from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.post import Post
from src.schemas.posts import PostUpdateSchema


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, post_id: int) -> Post | None:
        query = session.query(self._model).filter_by(id=post_id)
        return query.first()

    def get_all(self, session: Session) -> list[Post]:
        return session.query(self._model).all()

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Post]:
        return session.query(self._model).filter_by(author_id=author_id).all()

    def get_by_category(
        self,
        session: Session,
        category_id: int,
    ) -> list[Post]:
        return session.query(self._model).filter_by(
            category_id=category_id,
        ).all()

    def get_by_location(
        self,
        session: Session,
        location_id: int,
    ) -> list[Post]:
        return session.query(self._model).filter_by(
            location_id=location_id,
        ).all()

    def create(self, session: Session, post: Post) -> Post:
        session.add(post)
        session.commit()
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
        session.commit()
        session.refresh(post)
        return post

    def delete(self, session: Session, post: Post):
        session.delete(post)
        session.commit()
