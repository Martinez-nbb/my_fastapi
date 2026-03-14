from typing import Type

from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.user import User
from src.schemas.users import UserUpdateSchema


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, user_id: int) -> User | None:
        query = session.query(self._model).filter_by(id=user_id)
        return query.first()

    def get_by_username(
        self,
        session: Session,
        username: str,
    ) -> User | None:
        query = session.query(self._model).filter_by(username=username)
        return query.first()

    def get_all(self, session: Session) -> list[User]:
        return session.query(self._model).all()

    def create(self, session: Session, user: User) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def update(
        self,
        session: Session,
        user: User,
        data: UserUpdateSchema,
    ) -> User:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(user, field, value)
        session.commit()
        session.refresh(user)
        return user

    def delete(self, session: Session, user: User) -> None:
        session.delete(user)
        session.commit()
