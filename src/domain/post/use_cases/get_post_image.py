import os

from fastapi.responses import FileResponse

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.core.logging import get_logger

logger = get_logger(__name__)

MEDIA_TYPES = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostImageRepository()
        self.image_folder = "/app/images"

    async def execute(self, image_id: int) -> FileResponse:
        logger.info(f"Получение изображения: image_id={image_id}")

        async with self._database.session() as session:
            image = await self._repo.get(session=session, image_id=image_id)

        full_path = os.path.join(self.image_folder, image.file_path)
        if not os.path.exists(full_path):
            logger.error(f"Файл изображения не найден на диске: path={full_path}")
            raise FileNotFoundError(f"Image file not found: {image.file_path}")

        ext = image.file_path.rsplit('.', 1)[-1] if '.' in image.file_path else ''
        media_type = MEDIA_TYPES.get(ext, "image/jpeg")
        return FileResponse(full_path, media_type=media_type)
