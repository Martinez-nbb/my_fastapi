from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    handle_database_exception,
)
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentUpdateSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, comment_id: int) -> Comment:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            ).filter_by(id=comment_id)
            comment = query.first()
            if comment is None:
                raise CommentNotFoundException(f'Комментарий с id={comment_id} не найден')
            return comment
        except CommentNotFoundException:
            raise
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'комментарием')

    def get_all(self, session: Session) -> list[Comment]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'получением списка комментариев')

    def get_by_post(
        self,
        session: Session,
        post_id: int,
    ) -> list[Comment]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            ).filter_by(post_id=post_id)
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'поиском комментариев по посту')

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Comment]:
        try:
            query = session.query(self._model).options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            ).filter_by(author_id=author_id)
            return query.all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'поиском комментариев по автору')

    def create(self, session: Session, comment: Comment) -> Comment:
        try:
            session.add(comment)
            session.flush()
            session.refresh(comment)
            return comment
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'созданием комментария')

    def update(
        self,
        session: Session,
        comment: Comment,
        data: CommentUpdateSchema,
    ) -> Comment:
        try:
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(comment, field, value)
            session.flush()
            session.refresh(comment)
            return comment
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'обновлением комментария')

    def delete(self, session: Session, comment: Comment) -> None:
        try:
            session.delete(comment)
            session.flush()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'удалением комментария')
