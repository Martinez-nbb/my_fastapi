import logging
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
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.comments import CommentCreateSchema, CommentResponseSchema

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(
        self,
        data: CommentCreateSchema,
        author_id: int,
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            try:
                comment = self._repo.create(
                    session=session,
                    data=data,
                    author_id=author_id,
                )
            except UserNotFoundException:
                error = AuthorNotFoundException(author_id=author_id)
                logger.error(error.get_detail())
                raise error
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=data.post_id)
                logger.error(error.get_detail())
                raise error

            return CommentResponseSchema.model_validate(obj=comment)
