from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comment import CommentRepository
from src.schemas.comments import CommentResponseSchema


class GetCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[CommentResponseSchema]:
        async with self._database.session() as session:
            comments = await self._repo.get_all(session=session)
            result = []
            for comment in comments:
                schema = CommentResponseSchema.model_validate(obj=comment)
                result.append(schema)
            return result


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> list[CommentResponseSchema]:
        async with self._database.session() as session:
            comments = await self._repo.get_by_post(session=session, post_id=post_id)
            result = []
            for comment in comments:
                schema = CommentResponseSchema.model_validate(obj=comment)
                result.append(schema)
            return result
