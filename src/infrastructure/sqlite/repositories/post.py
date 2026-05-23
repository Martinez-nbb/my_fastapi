from datetime import datetime
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
    LocationNotFoundException,
    CategoryNotFoundException,
)
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.infrastructure.sqlite.models.user import User as UserModel
from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.posts import PostCreateSchema, PostUpdateSchema


class PostRepository:
    def __init__(self) -> None:
        self._model: Type[PostModel] = PostModel
        self._author_model: Type[UserModel] = UserModel
        self._location_model: Type[LocationModel] = LocationModel
        self._category_model: Type[CategoryModel] = CategoryModel

    def _eager_options(self):
        return (
            selectinload(self._model.author),
            selectinload(self._model.location),
            selectinload(self._model.category),
            selectinload(self._model.images),
        )

    async def get(self, session: AsyncSession, post_id: int) -> PostModel:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.id == post_id)
        )
        post = await session.scalar(query)

        if not post:
            raise PostNotFoundException()

        return post

    async def get_all(self, session: AsyncSession) -> list[PostModel]:
        query = select(self._model).options(*self._eager_options())
        result = await session.scalars(query)
        return list(result)

    async def get_by_author(self, session: AsyncSession, author_id: int) -> list[PostModel]:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.author_id == author_id)
        )
        result = await session.scalars(query)
        return list(result)

    async def get_by_category(
        self,
        session: AsyncSession,
        category_id: int,
    ) -> list[PostModel]:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.category_id == category_id)
        )
        result = await session.scalars(query)
        return list(result)

    async def get_by_location(
        self,
        session: AsyncSession,
        location_id: int,
    ) -> list[PostModel]:
        query = (
            select(self._model)
            .options(*self._eager_options())
            .where(self._model.location_id == location_id)
        )
        result = await session.scalars(query)
        return list(result)

    async def create(self, session: AsyncSession, data: PostCreateSchema) -> PostModel:
        author = await session.get(self._author_model, data.author_id)
        if not author:
            raise UserNotFoundException()

        if data.location_id is not None:
            location = await session.get(self._location_model, data.location_id)
            if not location:
                raise LocationNotFoundException()

        if data.category_id is not None:
            category = await session.get(self._category_model, data.category_id)
            if not category:
                raise CategoryNotFoundException()

        query = (
            insert(self._model)
            .values(
                title=data.title,
                text=data.text,
                pub_date=data.pub_date,
                author_id=data.author_id,
                location_id=data.location_id,
                category_id=data.category_id,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        post = await session.scalar(query)

        return post

    async def update(
        self,
        session: AsyncSession,
        post_id: int,
        data: PostUpdateSchema,
    ) -> PostModel:
        post = await self.get(session=session, post_id=post_id)

        update_data = data.model_dump(exclude_none=True)

        if 'author_id' in update_data and update_data['author_id'] != post.author_id:
            author = await session.get(self._author_model, update_data['author_id'])
            if not author:
                raise UserNotFoundException()

        if (
            'location_id' in update_data
            and update_data['location_id'] is not None
            and update_data['location_id'] != post.location_id
        ):
            location = await session.get(self._location_model, update_data['location_id'])
            if not location:
                raise LocationNotFoundException()

        if (
            'category_id' in update_data
            and update_data['category_id'] is not None
            and update_data['category_id'] != post.category_id
        ):
            category = await session.get(self._category_model, update_data['category_id'])
            if not category:
                raise CategoryNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == post_id)
            .values(**update_data)
            .returning(self._model)
        )
        post = await session.scalar(query)

        return post

    async def delete(self, session: AsyncSession, post_id: int) -> None:
        query = delete(self._model).where(self._model.id == post_id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise PostNotFoundException()
