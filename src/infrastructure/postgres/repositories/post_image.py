from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    PostImageNotFoundException,
    PostNotFoundException,
)
from src.infrastructure.postgres.models.post_image import PostImage as PostImageModel
from src.infrastructure.postgres.models.post import Post as PostModel
from src.schemas.posts import PostImageCreateSchema


class PostImageRepository:
    def __init__(self) -> None:
        self._model: Type[PostImageModel] = PostImageModel
        self._post_model: Type[PostModel] = PostModel

    async def get(self, session: AsyncSession, image_id: int) -> PostImageModel:
        query = select(self._model).where(self._model.id == image_id)
        image = await session.scalar(query)
        if not image:
            raise PostImageNotFoundException(image_id=image_id)
        return image

    async def get_by_post(self, session: AsyncSession, post_id: int) -> list[PostImageModel]:
        query = select(self._model).where(self._model.post_id == post_id)
        result = await session.scalars(query)
        return list(result)

    async def create(self, session: AsyncSession, data: PostImageCreateSchema) -> PostImageModel:
        post = await session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(
                post_id=data.post_id,
                file_path=data.file_path,
                original_name=data.original_name,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        image = await session.scalar(query)
        return image

    async def count_by_post(self, session: AsyncSession, post_id: int) -> int:
        query = select(func.count()).select_from(self._model).where(self._model.post_id == post_id)
        result = await session.scalar(query)
        return result or 0

    async def delete(self, session: AsyncSession, image_id: int) -> None:
        image = await self.get(session=session, image_id=image_id)
        query = delete(self._model).where(self._model.id == image_id)
        result = cast(CursorResult, await session.execute(query))
        if not result.rowcount:
            raise PostImageNotFoundException(image_id=image_id)
