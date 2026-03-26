import logging
from datetime import datetime

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import (
    LocationCreateSchema,
    LocationUpdateSchema,
    LocationResponseSchema,
)

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        data: LocationCreateSchema,
    ) -> LocationResponseSchema:
        logger.debug('Создание местоположения: name=%s', data.name)
        with self._database.session() as session:
            location = Location(
                name=data.name,
                is_published=data.is_published,
                created_at=datetime.now(),
            )
            self._repo.create(session=session, location=location)

        logger.info('Местоположение успешно создано: name=%s', data.name)
        return LocationResponseSchema.model_validate(obj=location)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        location_id: int,
        data: LocationUpdateSchema,
    ) -> LocationResponseSchema:
        logger.debug('Обновление местоположения: location_id=%s', location_id)
        with self._database.session() as session:
            try:
                location = self._repo.get(
                    session=session,
                    location_id=location_id,
                )
            except LocationNotFoundException as exc:
                logger.error(
                    'Местоположение не найдено для обновления: location_id=%s, ошибка: %s',
                    location_id,
                    exc,
                )
                raise LocationNotFoundByIdException(id=location_id)

            self._repo.update(
                session=session,
                location=location,
                data=data,
            )

        logger.info('Местоположение успешно обновлено: %s', location_id)
        return LocationResponseSchema.model_validate(obj=location)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        logger.debug('Удаление местоположения: location_id=%s', location_id)
        with self._database.session() as session:
            try:
                location = self._repo.get(
                    session=session,
                    location_id=location_id,
                )
            except LocationNotFoundException as exc:
                logger.error(
                    'Местоположение не найдено для удаления: location_id=%s, ошибка: %s',
                    location_id,
                    exc,
                )
                raise LocationNotFoundByIdException(id=location_id)

            self._repo.delete(session=session, location=location)

        logger.info('Местоположение успешно удалено: %s', location_id)
