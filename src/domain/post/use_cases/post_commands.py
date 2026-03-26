from datetime import datetime

from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    AuthorNotFoundException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, data: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                author = self._user_repo.get(
                    session=session,
                    user_id=data.author_id,
                )
            except UserNotFoundException:
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


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        with self._database.session() as session:
            try:
                post = self._repo.get(
                    session=session,
                    post_id=post_id,
                )
            except PostNotFoundException:
                raise PostNotFoundByIdException(id=post_id)

            self._repo.delete(session=session, post=post)
