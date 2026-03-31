import logging
from datetime import datetime

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationCreateSchema, LocationResponseSchema

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationCreateSchema) -> LocationResponseSchema:
        location = Location(
            name=data.name,
            is_published=data.is_published,
            created_at=datetime.now(),
        )

        with self._database.session() as session:
            self._repo.create(session=session, location=location)

        return LocationResponseSchema.model_validate(obj=location)
