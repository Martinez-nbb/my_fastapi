from src.core.config import settings
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.core.logging import get_logger
from src.domain.shared.async_file import async_remove_file
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comment import CommentRepository
from src.infrastructure.postgres.repositories.comment_image import CommentImageRepository
from src.infrastructure.postgres.repositories.post import PostRepository
from src.infrastructure.postgres.repositories.post_image import PostImageRepository
from src.infrastructure.postgres.repositories.user import UserRepository

logger = get_logger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()
        self._post_repo = PostRepository()
        self._comment_repo = CommentRepository()
        self._post_image_repo = PostImageRepository()
        self._comment_image_repo = CommentImageRepository()

    async def execute(self, user_id: int) -> None:
        logger.info(f"Удаление пользователя id={user_id}")

        async with self._database.session() as session:
            try:
                posts = await self._post_repo.get_by_author(session=session, author_id=user_id)
                comments = await self._comment_repo.get_by_author(session=session, author_id=user_id)

                post_image_files = []
                for post in posts:
                    images = await self._post_image_repo.get_by_post(session=session, post_id=post.id)
                    post_image_files.extend(img.file_path for img in images)

                comment_image_files = []
                for comment in comments:
                    images = await self._comment_image_repo.get_by_comment(session=session, comment_id=comment.id)
                    comment_image_files.extend(img.file_path for img in images)

                await self._repo.delete(session=session, user_id=user_id)
                logger.info(f"Пользователь id={user_id} успешно удален")
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error

        for fp in post_image_files:
            await async_remove_file(f"{settings.IMAGE_FOLDER}/{fp}")
        for fp in comment_image_files:
            await async_remove_file(f"{settings.IMAGE_FOLDER}/{fp}")
