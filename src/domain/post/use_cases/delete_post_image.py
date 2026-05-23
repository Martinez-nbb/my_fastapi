import logging

from src.core.config import settings
from src.core.exceptions.database_exceptions import PostImageNotFoundException
from src.core.exceptions.domain_exceptions import PostImageNotFoundByIdException
from src.domain.shared.async_file import async_remove_file
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.post_image import PostImageRepository

logger = logging.getLogger(__name__)


class DeletePostImageUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostImageRepository()

    async def execute(self, image_id: int) -> None:
        async with self._database.session() as session:
            try:
                image = await self._repo.get(session=session, image_id=image_id)
                file_path = f"{settings.IMAGE_FOLDER}/{image.file_path}"
                await self._repo.delete(session=session, image_id=image_id)
                await async_remove_file(file_path)
                logger.info(f"Post image deleted: image_id={image_id}, file={file_path}")
            except PostImageNotFoundException:
                error = PostImageNotFoundByIdException(id=image_id)
                logger.error(error.get_detail())
                raise error
