from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentResponseSchema


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, comment_id=comment_id)
            return CommentResponseSchema.model_validate(obj=comment)
