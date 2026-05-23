from typing import List
from uuid import uuid4

from fastapi import File, UploadFile

from src.schemas.posts import PostImageSchema, PostImageCreateSchema
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
)
from src.domain.shared.async_file import (
    async_write_file,
    async_remove_file,
    async_check_folder,
)
from src.core.logging import get_logger

logger = get_logger(__name__)


class AddPostImagesUseCase:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = PostImageRepository()

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

    async def execute(self, post_id: int, images: List[UploadFile]) -> List[PostImageSchema]:
        logger.info(f"Загрузка нескольких изображений для поста: post_id={post_id}, count={len(images)}")

        # Validate all images first
        validated_images = []
        for image in images:
            try:
                ext = self._validate_image(image)
                ext = "jpeg" if ext == "jpg" else ext
                new_image_name = str(uuid4())
                new_image_path = f"{self.image_folder}/{new_image_name}.{ext}"
                validated_images.append((image, ext, new_image_name, new_image_path))
            except (ValueError, UploadFileIsNotImageException):
                raise

        try:
            await async_check_folder(self.image_folder)

            results = []
            saved_paths = []
            # Process each image
            for image, ext, new_image_name, new_image_path in validated_images:
                try:
                    content = await image.read()
                    if not content:
                        logger.warning("Пустой файл изображения")
                        raise ImageFileReadException("Файл изображения пустой")

                    if len(content) > self.MAX_FILE_SIZE:
                        logger.warning(f"Файл слишком большой: size={len(content)}, max={self.MAX_FILE_SIZE}")
                        raise ImageFileSaveException(
                            f"Файл слишком большой (максимум {self.MAX_FILE_SIZE // (1024*1024)}MB)"
                        )

                    await async_write_file(new_image_path, content)
                    saved_paths.append(new_image_path)
                    logger.info(f"Файл сохранён: path={new_image_path}, size={len(content)}")

                    async with self._database.session() as session:
                        create_data = PostImageCreateSchema(
                            post_id=post_id,
                            file_path=f"{new_image_name}.{ext}",
                            original_name=getattr(image, 'filename', 'unknown'),
                        )
                        post_image = await self._repo.create(session=session, data=create_data)
                        logger.info(f"Изображение привязано к посту: post_id={post_id}, image_id={post_image.id}")

                    results.append(PostImageSchema.model_validate(post_image))

                except (IOError, OSError) as e:
                    logger.error(f"Ошибка записи файла: path={new_image_path}, error={str(e)}")
                    raise ImageFileSaveException(f"Не удалось сохранить файл: {str(e)}")
                except Exception as e:
                    logger.error(f"Ошибка сохранения в БД: post_id={post_id}, error={str(e)}")
                    raise

            return results

        except (
            PostNotFoundException,
            UploadFileIsNotImageException,
            ImageFileReadException,
            ImageFileSaveException,
            ImageFolderNotFoundException,
        ):
            for path in saved_paths:
                await async_remove_file(path)
            raise

        except Exception as e:
            for path in saved_paths:
                await async_remove_file(path)
            logger.error(f"Неожиданная ошибка при загрузке изображений: post_id={post_id}, error={str(e)}")
            raise