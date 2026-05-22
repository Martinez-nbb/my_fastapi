from datetime import datetime
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.schemas.locations import LocationCreateSchema, LocationUpdateSchema


class LocationRepository:
    def __init__(self) -> None:
        self._model: Type[LocationModel] = LocationModel

    async def get(self, session: AsyncSession, location_id: int) -> LocationModel:
        query = select(self._model).where(self._model.id == location_id)
        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    async def get_all(self, session: AsyncSession) -> list[LocationModel]:
        query = select(self._model)
        result = await session.scalars(query)
        return list(result)

    async def create(self, session: AsyncSession, data: LocationCreateSchema) -> LocationModel:
        query = (
            insert(self._model)
            .values(
                name=data.name,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            .returning(self._model)
        )
        location = await session.scalar(query)

        return location

    async def update(
        self,
        session: AsyncSession,
        location_id: int,
        data: LocationUpdateSchema,
    ) -> LocationModel:
        location = await self.get(session=session, location_id=location_id)

        update_data = data.model_dump(exclude_none=True)

        query = (
            update(self._model)
            .where(self._model.id == location_id)
            .values(**update_data)
            .returning(self._model)
        )
        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    async def delete(self, session: AsyncSession, location_id: int) -> None:
        query = delete(self._model).where(self._model.id == location_id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise LocationNotFoundException()
