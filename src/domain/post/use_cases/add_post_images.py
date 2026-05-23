from typing import List
from uuid import uuid4

from fastapi import UploadFile

from src.schemas.posts import PostImageSchema, PostImageCreateSchema
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.post_image import PostImageRepository
from src.core.config import settings
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    MaxImagesExceededException,
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
    ImageFolderNotWritableException,
)
from src.domain.shared.async_file import (
    async_write_file,
    async_remove_file,
    async_check_folder,
)
from src.domain.shared.image_utils import validate_image, MAX_FILE_SIZE
from src.core.logging import get_logger

logger = get_logger(__name__)


class AddPostImagesUseCase:
    def __init__(self) -> None:
        self.image_folder = settings.IMAGE_FOLDER
        self._database = database
        self._repo = PostImageRepository()

    MAX_IMAGES_PER_POST = 10

    async def execute(self, post_id: int, images: List[UploadFile]) -> List[PostImageSchema]:
        logger.info(f"Загрузка нескольких изображений для поста: post_id={post_id}, count={len(images)}")

        async with self._database.session() as session:
            current = await self._repo.count_by_post(session=session, post_id=post_id)
        if current + len(images) > self.MAX_IMAGES_PER_POST:
            raise ValueError(
                f"Превышен лимит изображений для поста: "
                f"уже {current}, добавляется {len(images)}, "
                f"максимум {self.MAX_IMAGES_PER_POST}"
            )

        validated_images = []
        for image in images:
            try:
                ext = validate_image(image)
                ext = "jpeg" if ext == "jpg" else ext
                new_image_name = str(uuid4())
                new_image_path = f"{self.image_folder}/{new_image_name}.{ext}"
                validated_images.append((image, ext, new_image_name, new_image_path))
            except (ValueError, UploadFileIsNotImageException):
                raise

        saved_paths = []
        try:
            await async_check_folder(self.image_folder)

            results = []
            for image, ext, new_image_name, new_image_path in validated_images:
                try:
                    content = await image.read()
                    if not content:
                        logger.warning("Пустой файл изображения")
                        raise ImageFileReadException("Файл изображения пустой")

                    if len(content) > MAX_FILE_SIZE:
                        logger.warning(f"Файл слишком большой: size={len(content)}, max={MAX_FILE_SIZE}")
                        raise ImageFileSaveException(
                            f"Файл слишком большой (максимум {MAX_FILE_SIZE // (1024*1024)}MB)"
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
                except PostNotFoundException:
                    raise PostNotFoundByIdException(id=post_id)
                except Exception as e:
                    logger.error(f"Ошибка сохранения в БД: post_id={post_id}, error={str(e)}")
                    raise

            return results

        except (
            PostNotFoundByIdException,
            UploadFileIsNotImageException,
            ImageFileReadException,
            ImageFileSaveException,
            ImageFolderNotFoundException,
            ImageFolderNotWritableException,
        ):
            for path in saved_paths:
                await async_remove_file(path)
            raise

        except Exception as e:
            for path in saved_paths:
                await async_remove_file(path)
            logger.error(f"Неожиданная ошибка при загрузке изображений: post_id={post_id}, error={str(e)}")
            raise
