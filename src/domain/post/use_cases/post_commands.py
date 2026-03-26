import logging
from datetime import datetime

from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
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

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, data: PostCreateSchema) -> PostResponseSchema:
        logger.debug(
            'Создание публикации: author_id=%s, title=%s',
            data.author_id,
            data.title,
        )
        with self._database.session() as session:
            try:
                author = self._user_repo.get(
                    session=session,
                    user_id=data.author_id,
                )
            except UserNotFoundException as exc:
                logger.error(
                    'Автор не найден для публикации: user_id=%s, ошибка: %s',
                    data.author_id,
                    exc,
                )
                raise UserNotFoundByIdException(id=data.author_id)

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

        logger.info('Публикация успешно создана: author_id=%s', data.author_id)
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
        logger.debug('Обновление публикации: post_id=%s', post_id)
        with self._database.session() as session:
            try:
                post = self._repo.get(
                    session=session,
                    post_id=post_id,
                )
            except PostNotFoundException as exc:
                logger.error(
                    'Публикация не найдена для обновления: post_id=%s, ошибка: %s',
                    post_id,
                    exc,
                )
                raise PostNotFoundByIdException(id=post_id)

            self._repo.update(
                session=session,
                post=post,
                data=data,
            )

        logger.info('Публикация успешно обновлена: %s', post_id)
        return PostResponseSchema.model_validate(obj=post)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        logger.debug('Удаление публикации: post_id=%s', post_id)
        with self._database.session() as session:
            try:
                post = self._repo.get(
                    session=session,
                    post_id=post_id,
                )
            except PostNotFoundException as exc:
                logger.error(
                    'Публикация не найдена для удаления: post_id=%s, ошибка: %s',
                    post_id,
                    exc,
                )
                raise PostNotFoundByIdException(id=post_id)

            self._repo.delete(session=session, post=post)

        logger.info('Публикация успешно удалена: %s', post_id)
