from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.posts import PostUpdateSchema, PostResponseSchema


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        post_id: int,
        data: PostUpdateSchema,
    ) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                post = self._repo.get(
                    session=session,
                    post_id=post_id,
                )
            except PostNotFoundException:
                raise PostNotFoundByIdException(id=post_id)

            self._repo.update(
                session=session,
                post=post,
                data=data,
            )

            return PostResponseSchema.model_validate(obj=post)
