import shutil
import os
from uuid import uuid4

from fastapi import File

from src.schemas.posts import PostImageResponse
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
)
from src.core.logging import get_logger

logger = get_logger(__name__)


class AddPostImageUseCase:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = PostRepository()

    ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "gif", "webp"}

    def _validate_image(self, image: File) -> str:
        if not hasattr(image, 'filename') or not image.filename:
            logger.warning("Отсутствует имя файла")
            raise ValueError("Filename is required")

        filename = image.filename.lower()
        ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''

        if ext not in self.ALLOWED_EXTENSIONS:
            logger.warning(f"Невалидное расширение файла: ext={ext}, filename={filename}")
            raise UploadFileIsNotImageException()

        return ext

    def _check_folder_exists(self) -> None:
        if not os.path.exists(self.image_folder):
            logger.error(f"Папка для изображений не существует: {self.image_folder}")
            raise ImageFolderNotFoundException(
                f"Папка для изображений не найдена: {self.image_folder}"
            )

    def _check_folder_writable(self) -> None:
        if not os.access(self.image_folder, os.W_OK):
            logger.error(f"Папка недоступна для записи: {self.image_folder}")
            raise ImageFileSaveException(
                f"Нет доступа к папке: {self.image_folder}"
            )

    async def execute(self, post_id: int, image: File) -> PostImageResponse:
        logger.info(f"Загрузка изображения для поста: post_id={post_id}, filename={getattr(image, 'filename', 'unknown')}")

        try:
            ext = self._validate_image(image)
            ext = "jpeg" if ext == "jpg" else ext
            new_image_name = str(uuid4())
            new_image_path = f"{self.image_folder}/{new_image_name}.{ext}"
        except (ValueError, UploadFileIsNotImageException):
            raise

        try:
            self._check_folder_exists()
            self._check_folder_writable()

            try:
                content = image.file.read()
                if not content:
                    logger.warning("Пустой файл изображения")
                    raise ImageFileReadException("Файл изображения пустой")

                if len(content) > self.MAX_FILE_SIZE:
                    logger.warning(f"Файл слишком большой: size={len(content)}, max={self.MAX_FILE_SIZE}")
                    raise ImageFileSaveException(
                        f"Файл слишком большой (максимум {self.MAX_FILE_SIZE // (1024*1024)}MB)"
                    )

                with open(new_image_path, "wb") as buffer:
                    buffer.write(content)

                logger.info(f"Файл сохранён: path={new_image_path}, size={len(content)}")

            except (IOError, OSError) as e:
                logger.error(f"Ошибка записи файла: path={new_image_path}, error={str(e)}")
                raise ImageFileSaveException(f"Не удалось сохранить файл: {str(e)}")

            try:
                with self._database.session() as session:
                    post = self._repo.get(session=session, post_id=post_id)
                    if not post:
                        logger.warning(f"Пост не найден: post_id={post_id}")
                        raise PostNotFoundException(detail=f"Post with id={post_id} not found")
                    post.image = new_image_name
                    session.commit()
                    logger.info(f"Изображение привязано к посту: post_id={post_id}, image={new_image_name}")

            except PostNotFoundException:
                raise
            except Exception as e:
                logger.error(f"Ошибка сохранения в БД: post_id={post_id}, error={str(e)}")
                raise

            return PostImageResponse(image_path=new_image_name)

        except (
            PostNotFoundException,
            UploadFileIsNotImageException,
            ImageFileReadException,
            ImageFileSaveException,
            ImageFolderNotFoundException,
        ):
            try:
                if 'new_image_path' in locals() and os.path.exists(new_image_path):
                    os.remove(new_image_path)
                    logger.debug(f"Файл удалён при ошибке: {new_image_path}")
            except Exception as e:
                logger.error(f"Не удалось удалить файл: error={str(e)}")
            raise

        except Exception as e:
            try:
                if 'new_image_path' in locals() and os.path.exists(new_image_path):
                    os.remove(new_image_path)
            except:
                pass
            logger.error(f"Неожиданная ошибка при загрузке изображения: post_id={post_id}, error={str(e)}")
            raise