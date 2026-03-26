import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationResponseSchema

logger = logging.getLogger(__name__)


class GetLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> list[LocationResponseSchema]:
        logger.debug('Получение списка всех местоположений')
        with self._database.session() as session:
            locations = self._repo.get_all(session=session)
        logger.debug('Получено местоположений: %s', len(locations))
        return [
            LocationResponseSchema.model_validate(obj=loc)
            for loc in locations
        ]
