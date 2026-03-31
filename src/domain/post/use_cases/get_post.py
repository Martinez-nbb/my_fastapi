from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.posts import PostResponseSchema


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.get(session=session, post_id=post_id)
            return PostResponseSchema.model_validate(obj=post)
