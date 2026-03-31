import logging

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationResponseSchema

logger = logging.getLogger(__name__)


class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationResponseSchema:
        try:
            with self._database.session() as session:
                location = self._repo.get(session=session, location_id=location_id)
        except LocationNotFoundException:
            error = LocationNotFoundByIdException(id=location_id)
            logger.error(error.get_detail())
            raise error

        return LocationResponseSchema.model_validate(obj=location)
