from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
    handle_database_exception,
)
from src.infrastructure.sqlite.models.user import User
from src.schemas.users import UserUpdateSchema


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, user_id: int) -> User:
        try:
            query = session.query(self._model).filter_by(id=user_id)
            user = query.first()
            if user is None:
                raise UserNotFoundException(f'Пользователь с идентификатором {user_id} не найден')
            return user
        except UserNotFoundException:
            raise
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'пользователь')

    def get_by_username(
        self,
        session: Session,
        username: str,
    ) -> User | None:
        try:
            query = session.query(self._model).filter_by(username=username)
            return query.first()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'пользователь')

    def get_by_email(
        self,
        session: Session,
        email: str,
    ) -> User | None:
        try:
            query = session.query(self._model).filter_by(email=email)
            return query.first()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'пользователь')

    def get_all(self, session: Session) -> list[User]:
        try:
            return session.query(self._model).all()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'пользователь')

    def create(self, session: Session, user: User) -> User:
        try:
            session.add(user)
            session.flush()
            session.refresh(user)
            return user
        except SQLAlchemyError as exc:
            if 'username' in str(exc.orig).lower():
                raise UserUsernameAlreadyExistsException(
                    f'Пользователь с именем {user.username} уже существует'
                )
            if 'email' in str(exc.orig).lower():
                raise UserEmailAlreadyExistsException(
                    f'Пользователь с email {user.email} уже существует'
                )
            raise handle_database_exception(exc, 'пользователь')

    def update(
        self,
        session: Session,
        user: User,
        data: UserUpdateSchema,
    ) -> User:
        try:
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(user, field, value)
            session.flush()
            session.refresh(user)
            return user
        except SQLAlchemyError as exc:
            if 'username' in str(exc.orig).lower():
                raise UserUsernameAlreadyExistsException(
                    f'Пользователь с именем {user.username} уже существует'
                )
            if 'email' in str(exc.orig).lower():
                raise UserEmailAlreadyExistsException(
                    f'Пользователь с email {user.email} уже существует'
                )
            raise handle_database_exception(exc, 'пользователь')

    def delete(self, session: Session, user: User) -> None:
        try:
            session.delete(user)
            session.flush()
        except SQLAlchemyError as exc:
            raise handle_database_exception(exc, 'пользователь')
