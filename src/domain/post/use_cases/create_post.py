import logging
from datetime import datetime

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    AuthorNotFoundException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.posts import PostCreateSchema, PostResponseSchema

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, data: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                post = self._repo.create(session=session, data=data)
            except UserNotFoundException:
                error = AuthorNotFoundException(author_id=data.author_id)
                logger.error(error.get_detail())
                raise error
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=data.location_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=data.category_id)
                logger.error(error.get_detail())
                raise error

            return PostResponseSchema.model_validate(obj=post)
