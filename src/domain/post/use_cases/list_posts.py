from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.posts import PostResponseSchema


class GetPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> list[PostResponseSchema]:
        with self._database.session() as session:
            posts = self._repo.get_all(session=session)
            return [
                PostResponseSchema.model_validate(obj=post)
                for post in posts
            ]
