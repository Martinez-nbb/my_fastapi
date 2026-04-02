import logging

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentUpdateSchema, CommentResponseSchema

logger = logging.getLogger(__name__)


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
                comment = self._repo.update(
                    session=session,
                    comment_id=comment_id,
                    data=data,
                )
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error
            except IntegrityError as e:
                logger.error(f"Ошибка IntegrityError при обновлении комментария: {e}")
                raise

            return CommentResponseSchema.model_validate(obj=comment)
