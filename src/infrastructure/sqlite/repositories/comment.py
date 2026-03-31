from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentUpdateSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, comment_id: int) -> Comment:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).where(self._model.id == comment_id)

        comment = session.scalar(query)
        if not comment:
            raise CommentNotFoundException()
        return comment

    def get_all(self, session: Session) -> list[Comment]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        )
        return list(session.scalars(query))

    def get_by_post(
        self,
        session: Session,
        post_id: int,
    ) -> list[Comment]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).where(self._model.post_id == post_id)
        return list(session.scalars(query))

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Comment]:
        query = select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).where(self._model.author_id == author_id)
        return list(session.scalars(query))

    def create(self, session: Session, comment: Comment) -> Comment:
        query = insert(self._model).values(
            text=comment.text,
            post_id=comment.post_id,
            author_id=comment.author_id,
            is_published=comment.is_published,
            created_at=comment.created_at,
        ).returning(self._model)

        try:
            created_comment = session.scalar(query)
            session.refresh(created_comment)
            return created_comment
        except IntegrityError:
            raise CommentNotFoundException()

    def update(
        self,
        session: Session,
        comment: Comment,
        data: CommentUpdateSchema,
    ) -> Comment:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(comment, field, value)
        session.flush()
        session.refresh(comment)
        return comment

    def delete(self, session: Session, comment: Comment) -> None:
        session.delete(comment)
        session.flush()
