import os
from fastapi.responses import FileResponse

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostHasNoImageException
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
        self._repo = PostRepository()
        self.image_folder = "/app/images"

    async def execute(self, post_id: int) -> FileResponse:
        logger.info(f"Получение изображения поста: post_id={post_id}")

        async with self._database.session() as session:
            try:
                post = await self._repo.get(session=session, post_id=post_id)

                if not post:
                    logger.warning(f"Пост не найден: post_id={post_id}")
                    raise PostNotFoundException(detail=f"Post with id={post_id} not found")

                image_path = post.image

                if not image_path:
                    logger.warning(f"У поста нет изображения: post_id={post_id}")
                    raise PostHasNoImageException(post_id=post_id)

            except (PostNotFoundException, PostHasNoImageException):
                raise
            except Exception as e:
                logger.error(f"Ошибка получения поста: post_id={post_id}, error={str(e)}")
                raise

        found_path = None
        found_ext = None
        for ext in ["jpeg", "jpg", "png", "gif", "webp"]:
            test_path = f"{self.image_folder}/{image_path}.{ext}"
            if os.path.exists(test_path):
                found_path = test_path
                found_ext = ext
                break

        if not found_path:
            logger.error(f"Файл изображения не найден на диске: path={image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")

        logger.info(f"Изображение найдено: post_id={post_id}, path={found_path}")

        media_type = MEDIA_TYPES.get(found_ext, "image/jpeg")
        return FileResponse(found_path, media_type=media_type)