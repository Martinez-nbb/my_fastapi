from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationUpdateSchema


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, location_id: int) -> Location:
        query = select(self._model).where(self._model.id == location_id)
        location = session.scalar(query)
        if not location:
            raise LocationNotFoundException()
        return location

    def get_all(self, session: Session) -> list[Location]:
        query = select(self._model)
        return list(session.scalars(query))

    def create(self, session: Session, location: Location) -> Location:
        query = insert(self._model).values(
            name=location.name,
            is_published=location.is_published,
            created_at=location.created_at,
        ).returning(self._model)

        try:
            created_location = session.scalar(query)
            session.refresh(created_location)
            return created_location
        except IntegrityError:
            raise LocationNotFoundException()

    def update(
        self,
        session: Session,
        location: Location,
        data: LocationUpdateSchema,
    ) -> Location:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(location, field, value)
        session.flush()
        session.refresh(location)
        return location

    def delete(self, session: Session, location: Location) -> None:
        session.delete(location)
        session.flush()
