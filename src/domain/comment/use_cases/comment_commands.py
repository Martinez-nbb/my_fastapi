from datetime import datetime

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentResponseSchema,
)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(
        self,
        data: CommentCreateSchema,
        author_id: int,
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            try:
                post = self._post_repo.get(
                    session=session,
                    post_id=data.post_id,
                )
            except PostNotFoundException as exc:
                raise PostNotFoundByIdException(id=data.post_id)

            comment = Comment(
                text=data.text,
                post_id=data.post_id,
                author_id=author_id,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            self._repo.create(session=session, comment=comment)

        return CommentResponseSchema.model_validate(obj=comment)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        comment_id: int,
        data: CommentUpdateSchema,
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            try:
                comment = self._repo.get(
                    session=session,
                    comment_id=comment_id,
                )
            except CommentNotFoundException as exc:
                raise CommentNotFoundByIdException(id=comment_id)

            self._repo.update(
                session=session,
                comment=comment,
                data=data,
            )

        return CommentResponseSchema.model_validate(obj=comment)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        with self._database.session() as session:
            try:
                comment = self._repo.get(
                    session=session,
                    comment_id=comment_id,
                )
            except CommentNotFoundException as exc:
                raise CommentNotFoundByIdException(id=comment_id)

            self._repo.delete(session=session, comment=comment)
