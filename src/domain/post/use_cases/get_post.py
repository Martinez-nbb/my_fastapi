import logging

from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.posts import PostResponseSchema

logger = logging.getLogger(__name__)


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        logger.debug('Получение публикации по id: %s', post_id)
        with self._database.session() as session:
            try:
                post = self._repo.get(
                    session=session,
                    post_id=post_id,
                )
            except PostNotFoundException as exc:
                logger.error(
                    'Публикация не найдена: post_id=%s, ошибка: %s',
                    post_id,
                    exc,
                )
                raise PostNotFoundByIdException(id=post_id)

        logger.debug('Публикация успешно получена: %s', post_id)
        return PostResponseSchema.model_validate(obj=post)
