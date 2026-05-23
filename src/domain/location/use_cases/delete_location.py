import logging

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.location import LocationRepository

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete(session=session, location_id=location_id)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error
