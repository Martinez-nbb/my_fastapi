from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.posts import PostCreateSchema, PostResponseSchema


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.get(session=session, post_id=post_id)

            if post is None:
                raise HTTPException(
                    status_code=404, detail=f'Публикация с id={post_id} не найдена'
                )

        return PostResponseSchema.model_validate(obj=post)


class GetPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> list[PostResponseSchema]:
        with self._database.session() as session:
            posts = self._repo.get_all(session=session)

        return [PostResponseSchema.model_validate(obj=post) for post in posts]


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, data: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            from src.infrastructure.sqlite.models.post import Post
            from datetime import datetime

            # Проверка существования автора
            author = self._user_repo.get(session=session, user_id=data.author_id)
            if author is None:
                raise HTTPException(
                    status_code=400, detail=f'Автор с id={data.author_id} не найден'
                )

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

    async def execute(self, post_id: int, data: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.get(session=session, post_id=post_id)

            if post is None:
                raise HTTPException(
                    status_code=404, detail=f'Публикация с id={post_id} не найдена'
                )

            self._repo.update(session=session, post=post, data=data)

        return PostResponseSchema.model_validate(obj=post)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int):
        with self._database.session() as session:
            post = self._repo.get(session=session, post_id=post_id)

            if post is None:
                raise HTTPException(
                    status_code=404, detail=f'Публикация с id={post_id} не найдена'
                )

            self._repo.delete(session=session, post=post)
