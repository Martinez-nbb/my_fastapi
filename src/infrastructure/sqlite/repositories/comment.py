from typing import Type

from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentUpdateSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, comment_id: int) -> Comment | None:
        query = session.query(self._model).filter_by(id=comment_id)
        return query.first()

    def get_all(self, session: Session) -> list[Comment]:
        return session.query(self._model).all()

    def get_by_post(
        self,
        session: Session,
        post_id: int,
    ) -> list[Comment]:
        return session.query(self._model).filter_by(post_id=post_id).all()

    def get_by_author(
        self,
        session: Session,
        author_id: int,
    ) -> list[Comment]:
        return session.query(self._model).filter_by(author_id=author_id).all()

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
