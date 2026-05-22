import os

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.core.exceptions.database_exceptions import PostImageNotFoundException
from src.core.logging import get_logger

logger = get_logger(__name__)


class DeletePostImageUseCase:
    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = PostImageRepository()

    async def execute(self, image_id: int) -> None:
        logger.info(f"Удаление изображения: image_id={image_id}")

        async with self._database.session() as session:
            image = await self._repo.get(session=session, image_id=image_id)
            file_path = os.path.join(self.image_folder, image.file_path)

            await self._repo.delete(session=session, image_id=image_id)

        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Файл удалён: {file_path}")
