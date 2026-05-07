import os

from fastapi.responses import FileResponse

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostHasNoImageException
from src.core.logging import get_logger

logger = get_logger(__name__)


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self.image_folder = "/app/images"

    async def execute(self, post_id: int) -> FileResponse:
        logger.info(f"Получение изображения поста: post_id={post_id}")
        
        with self._database.session() as session:
            try:
                post = self._repo.get(session=session, post_id=post_id)
                
                if not post:
                    logger.warning(f"Пост не найден: post_id={post_id}")
                    raise PostNotFoundException(detail=f"Post with id={post_id} not found")
                
                image_path = post.image
                
                if not image_path:
                    logger.warning(f"У поста нет изображения: post_id={post_id}")
                    raise PostHasNoImageException(post_id=post_id)
                    
            except PostNotFoundException:
                raise
            except PostHasNoImageException:
                raise
            except Exception as e:
                logger.error(f"Ошибка получения поста: post_id={post_id}, error={str(e)}")
                raise

        ext = image_path.split(".")[-1].lower()
        media_type = f"image/{'jpeg' if ext in ('jpeg', 'jpg') else ext}"
        
        full_image_path = f"{self.image_folder}/{image_path}"
        
        if not os.path.exists(full_image_path):
            logger.error(f"Файл изображения не найден на диске: path={full_image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        logger.info(f"Изображение найдено: post_id={post_id}, path={full_image_path}")

        return FileResponse(full_image_path, media_type=media_type)