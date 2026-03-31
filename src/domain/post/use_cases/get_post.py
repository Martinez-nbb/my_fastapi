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
        try:
            with self._database.session() as session:
                post = self._repo.get(session=session, post_id=post_id)
        except PostNotFoundException:
            error = PostNotFoundByIdException(id=post_id)
            logger.error(error.get_detail())
            raise error

        return PostResponseSchema.model_validate(obj=post)
