import logging

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import (
    LocationAlreadyExistsException,
    LocationNotFoundByIdException,
)
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.location import LocationRepository
from src.schemas.locations import LocationUpdateSchema, LocationResponseSchema

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        location_id: int,
        data: LocationUpdateSchema,
    ) -> LocationResponseSchema:
        async with self._database.session() as session:
            try:
                location = await self._repo.update(
                    session=session,
                    location_id=location_id,
                    data=data,
                )
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error
            except IntegrityError as e:
                logger.error(f"Ошибка IntegrityError при обновлении location: {e}")
                name = data.name if data.name else "неизвестно"
                raise LocationAlreadyExistsException(name=name)

            return LocationResponseSchema.model_validate(obj=location)
