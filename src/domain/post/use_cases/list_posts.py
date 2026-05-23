from src.domain.shared.enrich_image import build_media_type
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.posts import PostResponseSchema


class GetPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> list[PostResponseSchema]:
        async with self._database.session() as session:
            posts = await self._repo.get_all(session=session)
            result = []
            for post in posts:
                schema = PostResponseSchema.model_validate(obj=post)
                for img in schema.images:
                    img.media_type = build_media_type(img.file_path)
                result.append(schema)
            return result
