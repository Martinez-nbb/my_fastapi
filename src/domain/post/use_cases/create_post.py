from datetime import datetime

from src.core.exceptions.domain_exceptions import (
    AuthorNotFoundException,
    UserNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.posts import PostCreateSchema, PostResponseSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, data: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                self._user_repo.get(
                    session=session,
                    user_id=data.author_id,
                )
            except UserNotFoundByIdException:
                raise AuthorNotFoundException(author_id=data.author_id)

            post = Post(
                title=data.title,
                text=data.text,
                pub_date=data.pub_date,
                author_id=data.author_id,
                location_id=data.location_id,
                category_id=data.category_id,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            self._repo.create(session=session, post=post)

            return PostResponseSchema.model_validate(obj=post)
