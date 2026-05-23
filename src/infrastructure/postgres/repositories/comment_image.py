from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    CommentImageNotFoundException,
    CommentNotFoundException,
)
from src.infrastructure.postgres.models.comment_image import CommentImage as CommentImageModel
from src.infrastructure.postgres.models.comment import Comment as CommentModel
from src.schemas.comments import CommentImageCreateSchema


class CommentImageRepository:
    def __init__(self) -> None:
        self._model: Type[CommentImageModel] = CommentImageModel
        self._comment_model: Type[CommentModel] = CommentModel

    async def get(self, session: AsyncSession, image_id: int) -> CommentImageModel:
        query = select(self._model).where(self._model.id == image_id)
        image = await session.scalar(query)
        if not image:
            raise CommentImageNotFoundException(image_id=image_id)
        return image

    async def get_by_comment(self, session: AsyncSession, comment_id: int) -> list[CommentImageModel]:
        query = select(self._model).where(self._model.comment_id == comment_id)
        result = await session.scalars(query)
        return list(result)

    async def create(self, session: AsyncSession, data: CommentImageCreateSchema) -> CommentImageModel:
        comment = await session.get(self._comment_model, data.comment_id)
        if not comment:
            raise CommentNotFoundException()

        query = (
            insert(self._model)
            .values(
                comment_id=data.comment_id,
                file_path=data.file_path,
                original_name=data.original_name,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        image = await session.scalar(query)
        return image

    async def count_by_comment(self, session: AsyncSession, comment_id: int) -> int:
        query = select(func.count()).select_from(self._model).where(self._model.comment_id == comment_id)
        result = await session.scalar(query)
        return result or 0

    async def delete(self, session: AsyncSession, image_id: int) -> None:
        image = await self.get(session=session, image_id=image_id)
        query = delete(self._model).where(self._model.id == image_id)
        result = cast(CursorResult, await session.execute(query))
        if not result.rowcount:
            raise CommentImageNotFoundException(image_id=image_id)
