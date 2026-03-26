from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentResponseSchema


class GetCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[CommentResponseSchema]:
        with self._database.session() as session:
            comments = self._repo.get_all(session=session)
            return [
                CommentResponseSchema.model_validate(obj=comment)
                for comment in comments
            ]


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> list[CommentResponseSchema]:
        with self._database.session() as session:
            comments = self._repo.get_by_post(
                session=session,
                post_id=post_id,
            )
            return [
                CommentResponseSchema.model_validate(obj=comment)
                for comment in comments
            ]
