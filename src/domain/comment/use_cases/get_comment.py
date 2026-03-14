from datetime import datetime

from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.comments import CommentCreateSchema, CommentUpdateSchema, CommentResponseSchema


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, comment_id=comment_id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id={comment_id} не найден'
                )

            return CommentResponseSchema.model_validate(obj=comment)


class GetCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[CommentResponseSchema]:
        with self._database.session() as session:
            comments = self._repo.get_all(session=session)
            return [
                CommentResponseSchema.model_validate(obj=comment) for comment in comments
            ]


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> list[CommentResponseSchema]:
        with self._database.session() as session:
            comments = self._repo.get_by_post(session=session, post_id=post_id)
            return [
                CommentResponseSchema.model_validate(obj=comment) for comment in comments
            ]


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, data: CommentCreateSchema) -> CommentResponseSchema:
        with self._database.session() as session:
            post = self._post_repo.get(session=session, post_id=data.post_id)
            if post is None:
                raise HTTPException(
                    status_code=400, detail=f'Публикация с id={data.post_id} не найдена'
                )

            comment = Comment(
                text=data.text,
                post_id=data.post_id,
                author_id=data.author_id,
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
        self, comment_id: int, data: CommentUpdateSchema
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, comment_id=comment_id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id={comment_id} не найден'
                )

            self._repo.update(session=session, comment=comment, data=data)

            return CommentResponseSchema.model_validate(obj=comment)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int):
        with self._database.session() as session:
            comment = self._repo.get(session=session, comment_id=comment_id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id={comment_id} не найден'
                )

            self._repo.delete(session=session, comment=comment)
