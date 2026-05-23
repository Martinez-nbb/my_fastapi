import logging

from src.core.config import settings
from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.domain.shared.async_file import async_remove_file
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comment import CommentRepository
from src.infrastructure.postgres.repositories.comment_image import CommentImageRepository

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._image_repo = CommentImageRepository()

    async def execute(self, comment_id: int) -> None:
        async with self._database.session() as session:
            try:
                images = await self._image_repo.get_by_comment(session=session, comment_id=comment_id)
                await self._repo.delete(session=session, comment_id=comment_id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error

        for img in images:
            await async_remove_file(f"{settings.IMAGE_FOLDER}/{img.file_path}")
            logger.info(f"Image file removed: {img.file_path}")
