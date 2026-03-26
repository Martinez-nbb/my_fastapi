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
        logger.debug('Получение комментария по id: %s', comment_id)
        with self._database.session() as session:
            try:
                comment = self._repo.get(
                    session=session,
                    comment_id=comment_id,
                )
            except CommentNotFoundException as exc:
                logger.error(
                    'Комментарий не найден: comment_id=%s, ошибка: %s',
                    comment_id,
                    exc,
                )
                raise CommentNotFoundByIdException(id=comment_id)

        logger.debug('Комментарий успешно получен: %s', comment_id)
        return CommentResponseSchema.model_validate(obj=comment)
