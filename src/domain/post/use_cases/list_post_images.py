from src.schemas.posts import PostImageSchema, PostImageResponseSchema
from src.domain.shared.enrich_image import enrich_image_data, build_media_type
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class ListPostImagesUseCase:
    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = PostImageRepository()

    async def execute(self, post_id: int) -> list[PostImageResponseSchema]:
        logger.info(f"Получение списка изображений поста: post_id={post_id}")

        async with self._database.session() as session:
            images = await self._repo.get_by_post(session=session, post_id=post_id)

        result = []
        for img in images:
            full = PostImageSchema.model_validate(img)
            result.append(PostImageResponseSchema(
                id=full.id,
                data=await enrich_image_data(full.file_path, self.image_folder),
                media_type=build_media_type(full.file_path),
            ))

        return result