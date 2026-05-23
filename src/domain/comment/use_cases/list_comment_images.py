from src.schemas.comments import CommentImageSchema, CommentImageResponseSchema
from src.domain.shared.enrich_image import enrich_image_data, build_media_type
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_image import CommentImageRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class ListCommentImagesUseCase:
    def __init__(self) -> None:
        self.image_folder = "/app/images"
        self._database = database
        self._repo = CommentImageRepository()

    async def execute(self, comment_id: int) -> list[CommentImageResponseSchema]:
        logger.info(f"Получение списка изображений комментария: comment_id={comment_id}")

        async with self._database.session() as session:
            images = await self._repo.get_by_comment(session=session, comment_id=comment_id)

        result = []
        for img in images:
            full = CommentImageSchema.model_validate(img)
            result.append(CommentImageResponseSchema(
                id=full.id,
                data=await enrich_image_data(full.file_path, self.image_folder),
                media_type=build_media_type(full.file_path),
            ))

        return result