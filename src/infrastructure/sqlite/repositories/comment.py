from datetime import datetime
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from src.infrastructure.sqlite.models.comment import Comment as CommentModel
from src.infrastructure.sqlite.models.user import User as UserModel
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.schemas.comments import CommentCreateSchema, CommentUpdateSchema


class CommentRepository:
    def __init__(self) -> None:
        self._model: Type[CommentModel] = CommentModel
        self._author_model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel

    def get(self, session: Session, comment_id: int) -> CommentModel:
        query = select(self._model).where(self._model.id == comment_id)
        comment = session.scalar(query)

        if not comment:
            raise CommentNotFoundException()

        return comment

    def get_all(self, session: Session) -> list[CommentModel]:
        query = select(self._model)
        return list(session.scalars(query))

    def get_by_post(self, session: Session, post_id: int) -> list[CommentModel]:
        query = select(self._model).where(self._model.post_id == post_id)
        return list(session.scalars(query))

    def get_by_author(self, session: Session, author_id: int) -> list[CommentModel]:
        query = select(self._model).where(self._model.author_id == author_id)
        return list(session.scalars(query))

    def create(self, session: Session, data: CommentCreateSchema, author_id: int) -> CommentModel:
        author = session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        post = session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(
                text=data.text,
                post_id=data.post_id,
                author_id=author_id,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    def update(
        self,
        session: Session,
        comment_id: int,
        data: CommentUpdateSchema,
    ) -> CommentModel:
        comment = self.get(session=session, comment_id=comment_id)

        update_data = data.model_dump(exclude_none=True)

        if (
            'author_id' in update_data
            and update_data['author_id'] != comment.author_id
        ):
            author = session.get(self._author_model, update_data['author_id'])
            if not author:
                raise UserNotFoundException()

        if (
            'post_id' in update_data
            and update_data['post_id'] != comment.post_id
        ):
            post = session.get(self._post_model, update_data['post_id'])
            if not post:
                raise PostNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(**update_data)
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    def delete(self, session: Session, comment_id: int) -> None:
        query = delete(self._model).where(self._model.id == comment_id)
        result = cast(CursorResult, session.execute(query))

        if not result.rowcount:
            raise CommentNotFoundException()
