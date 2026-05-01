import bcrypt
from typing import Type, cast

from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
)
from src.infrastructure.sqlite.models.user import User as UserModel
from src.schemas.users import UserCreateSchema, UserUpdateSchema


class UserRepository:
    def __init__(self) -> None:
        self._model: Type[UserModel] = UserModel

    def get(self, session: Session, user_id: int) -> UserModel:
        query = select(self._model).where(self._model.id == user_id)
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def get_by_username(self, session: Session, username: str) -> UserModel:
        query = select(self._model).where(self._model.username == username)
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def get_by_email(self, session: Session, email: str) -> UserModel:
        query = select(self._model).where(self._model.email == email)
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def get_all(self, session: Session) -> list[UserModel]:
        query = select(self._model)
        return list(session.scalars(query))

    def create(self, session: Session, data: UserCreateSchema) -> UserModel:
        existing_user = session.scalar(
            select(self._model).where(
                (self._model.username == data.username) |
                (self._model.email == (data.email or ''))
            )
        )

        if existing_user is not None:
            if existing_user.username == data.username:
                raise UserUsernameAlreadyExistsException()
            elif existing_user.email == (data.email or ''):
                raise UserEmailAlreadyExistsException()

        password_hash = data.password.get_secret_value()

        query = (
            insert(self._model)
            .values(
                username=data.username,
                password=password_hash,
                email=data.email or '',
                first_name=data.first_name or '',
                last_name=data.last_name or '',
                is_active=True,
            )
            .returning(self._model)
        )
        user = session.scalar(query)

        return user

    def update(
        self,
        session: Session,
        user_id: int,
        data: UserUpdateSchema,
    ) -> UserModel:
        user = self.get(session=session, user_id=user_id)

        update_data = data.model_dump(exclude_none=True)

        if 'email' in update_data and update_data['email'] != user.email:
            existing_email = session.scalar(
                select(self._model).where(
                    self._model.email == update_data['email'],
                    self._model.id != user_id,
                )
            )
            if existing_email:
                raise UserEmailAlreadyExistsException()

        if 'username' in update_data and update_data['username'] != user.username:
            existing_username = session.scalar(
                select(self._model).where(
                    self._model.username == update_data['username'],
                    self._model.id != user_id,
                )
            )
            if existing_username:
                raise UserUsernameAlreadyExistsException()

        query = (
            update(self._model)
            .where(self._model.id == user_id)
            .values(**update_data)
            .returning(self._model)
        )
        user = session.scalar(query)

        return user

    def delete(self, session: Session, user_id: int) -> None:
        query = delete(self._model).where(self._model.id == user_id)
        result = cast(CursorResult, session.execute(query))

        if not result.rowcount:
            raise UserNotFoundException()
