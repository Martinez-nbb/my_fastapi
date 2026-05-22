import os

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_image import CommentImageRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class DeleteCommentImageUseCase:
    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = CommentImageRepository()

    async def execute(self, image_id: int) -> None:
        logger.info(f"Удаление изображения комментария: image_id={image_id}")

        async with self._database.session() as session:
            image = await self._repo.get(session=session, image_id=image_id)
            file_path = os.path.join(self.image_folder, image.file_path)

            await self._repo.delete(session=session, image_id=image_id)

        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Файл удалён: {file_path}")
