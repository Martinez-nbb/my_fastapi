from src.schemas.posts import PostImageSchema
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class ListPostImagesUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostImageRepository()

    async def execute(self, post_id: int) -> list[PostImageSchema]:
        logger.info(f"Получение списка изображений поста: post_id={post_id}")

        async with self._database.session() as session:
            images = await self._repo.get_by_post(session=session, post_id=post_id)

        return [PostImageSchema.model_validate(img) for img in images]
