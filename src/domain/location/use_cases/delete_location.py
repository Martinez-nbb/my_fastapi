from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        with self._database.session() as session:
            location = self._repo.get(session=session, location_id=location_id)
            self._repo.delete(session=session, location=location)
