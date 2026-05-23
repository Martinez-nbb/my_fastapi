from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from src.infrastructure.postgres.models.comment import Comment as CommentModel
from src.infrastructure.postgres.models.user import User as UserModel
from src.infrastructure.postgres.models.post import Post as PostModel
from src.schemas.comments import CommentCreateSchema, CommentUpdateSchema


class CommentRepository:
    def __init__(self) -> None:
        self._model: Type[CommentModel] = CommentModel
        self._author_model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel

    def _eager_options(self):
        return (
            selectinload(self._model.author),
            selectinload(self._model.images),
        )

    async def get(self, session: AsyncSession, comment_id: int) -> CommentModel:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.id == comment_id)
        )
        comment = await session.scalar(query)

        if not comment:
            raise CommentNotFoundException()

        return comment

    async def get_all(self, session: AsyncSession) -> list[CommentModel]:
        query = select(self._model).options(*self._eager_options())
        result = await session.scalars(query)
        return list(result)

    async def get_by_post(self, session: AsyncSession, post_id: int) -> list[CommentModel]:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.post_id == post_id)
        )
        result = await session.scalars(query)
        return list(result)

    async def get_by_author(self, session: AsyncSession, author_id: int) -> list[CommentModel]:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.author_id == author_id)
        )
        result = await session.scalars(query)
        return list(result)

    async def create(self, session: AsyncSession, data: CommentCreateSchema, author_id: int) -> CommentModel:
        author = await session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        post = await session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(
                text=data.text,
                post_id=data.post_id,
                author_id=author_id,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        comment = await session.scalar(query)

        return comment

    async def update(
        self,
        session: AsyncSession,
        comment_id: int,
        data: CommentUpdateSchema,
    ) -> CommentModel:
        comment = await self.get(session=session, comment_id=comment_id)

        update_data = data.model_dump(exclude_none=True)

        if (
            'author_id' in update_data
            and update_data['author_id'] != comment.author_id
        ):
            author = await session.get(self._author_model, update_data['author_id'])
            if not author:
                raise UserNotFoundException()

        if (
            'post_id' in update_data
            and update_data['post_id'] != comment.post_id
        ):
            post = await session.get(self._post_model, update_data['post_id'])
            if not post:
                raise PostNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == comment_id)
            .values(**update_data)
            .returning(self._model)
        )
        comment = await session.scalar(query)

        return comment

    async def delete(self, session: AsyncSession, comment_id: int) -> None:
        query = delete(self._model).where(self._model.id == comment_id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise CommentNotFoundException()
