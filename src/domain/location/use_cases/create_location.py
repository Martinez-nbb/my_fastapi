import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationCreateSchema, LocationResponseSchema

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationCreateSchema) -> LocationResponseSchema:
        with self._database.session() as session:
            try:
                location = self._repo.create(session=session, data=data)
            except IntegrityError as e:
                logger.error(f"Ошибка IntegrityError при создании location: {e}")
                raise

            return LocationResponseSchema.model_validate(obj=location)
