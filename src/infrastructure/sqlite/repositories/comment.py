from typing import Type

from sqlalchemy.orm import Session, joinedload

from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentUpdateSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, comment_id: int) -> Comment:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).filter_by(id=comment_id)
        comment = query.first()
        if comment is None:
            raise CommentNotFoundException(
                f'Комментарий с id={comment_id} не найден'
            )
        return comment

    def get_all(self, session: Session) -> list[Comment]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        )
        return query.all()

    def get_by_post(
        self,
        session: Session,
        post_id: int,
    ) -> list[Comment]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).filter_by(post_id=post_id)
        return query.all()

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Comment]:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).filter_by(author_id=author_id)
        return query.all()

    def create(self, session: Session, comment: Comment) -> Comment:
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment

    def update(
        self,
        session: Session,
        comment: Comment,
        data: CommentUpdateSchema,
    ) -> Comment:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(comment, field, value)
        session.commit()
        session.refresh(comment)
        return comment

    def delete(self, session: Session, comment: Comment) -> None:
        session.delete(comment)
        session.commit()
