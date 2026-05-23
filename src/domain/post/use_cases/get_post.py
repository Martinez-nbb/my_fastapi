import logging

from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.domain.shared.enrich_image import build_media_type
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.posts import PostResponseSchema

logger = logging.getLogger(__name__)


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._repo.get(session=session, post_id=post_id)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error

            schema = PostResponseSchema.model_validate(obj=post)
            for img in schema.images:
                img.media_type = build_media_type(img.file_path)
            return schema