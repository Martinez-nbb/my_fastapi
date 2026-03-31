import logging

from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentResponseSchema

logger = logging.getLogger(__name__)


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponseSchema:
        try:
            with self._database.session() as session:
                comment = self._repo.get(session=session, comment_id=comment_id)
        except CommentNotFoundException:
            error = CommentNotFoundByIdException(id=comment_id)
            logger.error(error.get_detail())
            raise error

        return CommentResponseSchema.model_validate(obj=comment)
