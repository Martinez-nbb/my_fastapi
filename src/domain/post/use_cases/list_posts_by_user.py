from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.post import PostRepository
from src.schemas.posts import PostResponseSchema


class GetPostsByUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, user_id: int) -> list[PostResponseSchema]:
        async with self._database.session() as session:
            posts = await self._repo.get_by_author(session=session, author_id=user_id)
            return [PostResponseSchema.model_validate(p) for p in posts]
