import logging

from src.core.config import settings
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.domain.shared.async_file import async_remove_file
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.post import PostRepository
from src.infrastructure.postgres.repositories.post_image import PostImageRepository

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._image_repo = PostImageRepository()

    async def execute(self, post_id: int) -> None:
        async with self._database.session() as session:
            try:
                images = await self._image_repo.get_by_post(session=session, post_id=post_id)
                await self._repo.delete(session=session, post_id=post_id)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error

        for img in images:
            await async_remove_file(f"{settings.IMAGE_FOLDER}/{img.file_path}")
            logger.info(f"Image file removed: {img.file_path}")
