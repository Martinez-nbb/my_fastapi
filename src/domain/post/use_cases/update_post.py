import logging

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    LocationNotFoundException,
    CategoryNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    LocationNotFoundByIdException,
    CategoryNotFoundByIdException,
)
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.post import PostRepository
from src.schemas.posts import PostUpdateSchema, PostResponseSchema

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        post_id: int,
        data: PostUpdateSchema,
    ) -> PostResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._repo.update(
                    session=session,
                    post_id=post_id,
                    data=data,
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            except LocationNotFoundException as exc:
                raise LocationNotFoundByIdException(id=data.location_id)
            except CategoryNotFoundException as exc:
                raise CategoryNotFoundByIdException(id=data.category_id)
            except IntegrityError as e:
                logger.error(f"Ошибка IntegrityError при обновлении поста: {e}")
                raise

            return PostResponseSchema.model_validate(obj=post)
