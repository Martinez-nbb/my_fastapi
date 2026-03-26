from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentUpdateSchema, CommentResponseSchema


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        comment_id: int,
        data: CommentUpdateSchema,
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            try:
                comment = self._repo.get(
                    session=session,
                    comment_id=comment_id,
                )
            except CommentNotFoundException:
                raise CommentNotFoundByIdException(id=comment_id)

            self._repo.update(
                session=session,
                comment=comment,
                data=data,
            )

            return CommentResponseSchema.model_validate(obj=comment)
