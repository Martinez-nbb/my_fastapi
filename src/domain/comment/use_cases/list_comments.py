import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentResponseSchema

logger = logging.getLogger(__name__)


class GetCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[CommentResponseSchema]:
        logger.debug('Получение списка всех комментариев')
        with self._database.session() as session:
            comments = self._repo.get_all(session=session)
        logger.debug('Получено комментариев: %s', len(comments))
        return [
            CommentResponseSchema.model_validate(obj=comment)
            for comment in comments
        ]


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> list[CommentResponseSchema]:
        logger.debug('Получение комментариев по посту: post_id=%s', post_id)
        with self._database.session() as session:
            comments = self._repo.get_by_post(
                session=session,
                post_id=post_id,
            )
        logger.debug('Получено комментариев для поста %s: %s', post_id, len(comments))
        return [
            CommentResponseSchema.model_validate(obj=comment)
            for comment in comments
        ]
