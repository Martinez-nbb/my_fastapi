from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    LocationNotFoundException,
    handle_database_exception,
)
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationUpdateSchema


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, location_id: int) -> Location:
        try:
            query = session.query(self._model).filter_by(id=location_id)
            location = query.first()
            if location is None:
                raise LocationNotFoundException(f'Местоположение с id={location_id} не найдено')
            return location
        except LocationNotFoundException:
            raise
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'местоположением')

    def get_all(self, session: Session) -> list[Location]:
        try:
            return session.query(self._model).all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'получением списка местоположений')

    def create(self, session: Session, location: Location) -> Location:
        try:
            session.add(location)
            session.flush()
            session.refresh(location)
            return location
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'созданием местоположения')

    def update(
        self,
        session: Session,
        location: Location,
        data: LocationUpdateSchema,
    ) -> Location:
        try:
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(location, field, value)
            session.flush()
            session.refresh(location)
            return location
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'обновлением местоположения')

    def delete(self, session: Session, location: Location) -> None:
        try:
            session.delete(location)
            session.flush()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'удалением местоположения')
