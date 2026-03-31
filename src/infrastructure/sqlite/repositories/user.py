from typing import Type

from sqlalchemy.orm import Session

from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserNotFoundByEmailException,
)
from src.infrastructure.sqlite.models.user import User
from src.schemas.users import UserUpdateSchema


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, user_id: int) -> User:
        query = session.query(self._model).filter_by(id=user_id)
        user = query.first()
        if user is None:
            raise UserNotFoundByIdException(id=user_id)
        return user

    def get_by_username(
        self,
        session: Session,
        username: str,
    ) -> User:
        query = session.query(self._model).filter_by(username=username)
        user = query.first()
        if user is None:
            raise UserNotFoundByUsernameException(username=username)
        return user

    def get_by_email(
        self,
        session: Session,
        email: str,
    ) -> User:
        query = session.query(self._model).filter_by(email=email)
        user = query.first()
        if user is None:
            raise UserNotFoundByEmailException(email=email)
        return user

    def get_all(self, session: Session) -> list[User]:
        return session.query(self._model).all()

    def create(self, session: Session, user: User) -> User:
        session.add(user)
        session.flush()
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
        session.flush()
        session.refresh(user)
        return user

    def delete(self, session: Session, user: User) -> None:
        session.delete(user)
        session.flush()
