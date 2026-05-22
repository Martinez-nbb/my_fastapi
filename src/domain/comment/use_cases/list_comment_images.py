from src.schemas.comments import CommentImageSchema
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_image import CommentImageRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class ListCommentImagesUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentImageRepository()

    async def execute(self, comment_id: int) -> list[CommentImageSchema]:
        logger.info(f"Получение списка изображений комментария: comment_id={comment_id}")

        async with self._database.session() as session:
            images = await self._repo.get_by_comment(session=session, comment_id=comment_id)

        return [CommentImageSchema.model_validate(img) for img in images]
