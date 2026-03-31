import logging

from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        try:
            with self._database.session() as session:
                post = self._repo.get(session=session, post_id=post_id)
                self._repo.delete(session=session, post=post)
        except PostNotFoundException:
            error = PostNotFoundByIdException(id=post_id)
            logger.error(error.get_detail())
            raise error
