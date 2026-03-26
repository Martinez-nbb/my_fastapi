from typing import Type

from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationUpdateSchema


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, location_id: int) -> Location:
        query = session.query(self._model).filter_by(id=location_id)
        location = query.first()
        if location is None:
            raise LocationNotFoundException(
                f'Местоположение с id={location_id} не найдено'
            )
        return location

    def get_all(self, session: Session) -> list[Location]:
        return session.query(self._model).all()

    def create(self, session: Session, location: Location) -> Location:
        session.add(location)
        session.commit()
        session.refresh(location)
        return location

    def update(
        self,
        session: Session,
        location: Location,
        data: LocationUpdateSchema,
    ) -> Location:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(location, field, value)
        session.commit()
        session.refresh(location)
        return location

    def delete(self, session: Session, location: Location) -> None:
        session.delete(location)
        session.commit()
