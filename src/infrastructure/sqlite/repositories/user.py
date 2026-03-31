from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from src.infrastructure.sqlite.models.user import User
from src.schemas.users import UserUpdateSchema


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, user_id: int) -> User:
        query = select(self._model).where(self._model.id == user_id)
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    def get_by_username(
        self,
        session: Session,
        username: str,
    ) -> User:
        query = select(self._model).where(self._model.username == username)
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    def get_by_email(
        self,
        session: Session,
        email: str,
    ) -> User:
        query = select(self._model).where(self._model.email == email)
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    def get_all(self, session: Session) -> list[User]:
        query = select(self._model)
        return list(session.scalars(query))

    def create(self, session: Session, user: User) -> User:
        query = insert(self._model).values(
            username=user.username,
            password=user.password,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
        ).returning(self._model)

        try:
            created_user = session.scalar(query)
            session.refresh(created_user)
            return created_user
        except IntegrityError:
            raise UserAlreadyExistsException()

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
