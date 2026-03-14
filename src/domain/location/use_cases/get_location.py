from datetime import datetime

from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationCreateSchema, LocationUpdateSchema, LocationResponseSchema


class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._repo.get(session=session, location_id=location_id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id={location_id} не найдено'
                )

            return LocationResponseSchema.model_validate(obj=location)


class GetLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> list[LocationResponseSchema]:
        with self._database.session() as session:
            locations = self._repo.get_all(session=session)
            return [
                LocationResponseSchema.model_validate(obj=loc) for loc in locations
            ]


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationCreateSchema) -> LocationResponseSchema:
        with self._database.session() as session:
            location = Location(
                name=data.name,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            self._repo.create(session=session, location=location)

            return LocationResponseSchema.model_validate(obj=location)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, location_id: int, data: LocationUpdateSchema
    ) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._repo.get(session=session, location_id=location_id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id={location_id} не найдено'
                )

            self._repo.update(session=session, location=location, data=data)

            return LocationResponseSchema.model_validate(obj=location)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int):
        with self._database.session() as session:
            location = self._repo.get(session=session, location_id=location_id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id={location_id} не найдено'
                )

            self._repo.delete(session=session, location=location)
