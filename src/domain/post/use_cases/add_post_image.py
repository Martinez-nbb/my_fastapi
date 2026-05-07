import shutil
import os
from uuid import uuid4

from fastapi import UploadFile

from src.schemas.posts import PostImageResponse
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.logging import get_logger

logger = get_logger(__name__)


class AddPostImageUseCase:
    ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, image: UploadFile) -> PostImageResponse:
        logger.info(f"Загрузка изображения для поста: post_id={post_id}, filename={image.filename}")
        
        if not hasattr(image, 'filename') or not image.filename:
            logger.warning(f"Отсутствует имя файла для поста {post_id}")
            raise ValueError("Filename is required")

        filename = image.filename.lower()
        parts = filename.rsplit('.', 1)
        
        if len(parts) < 2:
            logger.warning(f"Файл без расширения: post_id={post_id}, filename={image.filename}")
            raise ValueError("Image must have a valid extension (jpeg, jpg, png)")
        
        ext = parts[-1]
        
        if ext not in self.ALLOWED_EXTENSIONS:
            logger.warning(f"Невалидное расширение файла: post_id={post_id}, ext={ext}")
            raise ValueError(f"Image must be JPEG or PNG. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}")

        if hasattr(image, 'content_type') and image.content_type:
            if image.content_type not in self.ALLOWED_MIME_TYPES:
                logger.warning(f"Невалидный content_type: post_id={post_id}, type={image.content_type}")
                raise ValueError(f"Invalid image type: {image.content_type}. Allowed: image/jpeg, image/png")

        new_image_name = str(uuid4())
        new_image_path = f"{self.image_folder}/{new_image_name}.{ext}"

        try:
            content = await image.read()
            
            if len(content) == 0:
                logger.warning(f"Пустой файл изображения: post_id={post_id}")
                raise ValueError("Image file is empty")
            
            if len(content) > self.MAX_FILE_SIZE:
                logger.warning(f"Файл слишком большой: post_id={post_id}, size={len(content)}")
                raise ValueError(f"Image file is too large (max {self.MAX_FILE_SIZE // (1024*1024)}MB)")

            logger.debug(f"Сохранение файла: path={new_image_path}, size={len(content)}")
            
            with open(new_image_path, "wb") as buffer:
                buffer.write(content)

            image_path = f"{new_image_name}.{ext}"

            with self._database.session() as session:
                try:
                    post = self._repo.get(session=session, post_id=post_id)
                    if not post:
                        logger.warning(f"Пост не найден: post_id={post_id}")
                        raise PostNotFoundException(detail=f"Post with id={post_id} not found")
                    post.image = image_path
                    session.commit()
                    logger.info(f"Изображение привязано к посту: post_id={post_id}, image={image_path}")
                except Exception as e:
                    session.rollback()
                    logger.error(f"Ошибка сохранения в БД: post_id={post_id}, error={str(e)}")
                    raise

            return PostImageResponse(image_path=image_path)
            
        except PostNotFoundException:
            self._cleanup_file(new_image_path)
            raise
        except ValueError:
            self._cleanup_file(new_image_path)
            raise
        except Exception as e:
            self._cleanup_file(new_image_path)
            logger.error(f"Неожиданная ошибка при загрузке изображения: post_id={post_id}, error={str(e)}")
            raise ValueError(f"Failed to save image: {str(e)}")

    def _cleanup_file(self, filepath: str) -> None:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.debug(f"Удалён файл при ошибке: {filepath}")
        except Exception as e:
            logger.error(f"Не удалось удалить файл: {filepath}, error={str(e)}")