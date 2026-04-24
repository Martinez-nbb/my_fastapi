from typing import Annotated
from fastapi import Depends
from jose import JWTError, jwt

from src.core.config import settings
from src.schemas.users import UserResponseSchema
from src.resources.auth import oauth2_scheme, optional_oauth2_scheme
from src.infrastructure.sqlite.database import database, Database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.auth_exceptions import CredentialsException


class AuthService:
    @staticmethod
    async def _resolve_user_from_token(token: str) -> UserResponseSchema:
        _AUTH_EXCEPTION_MESSAGE = 'Невозможно проверить данные авторизации'
        _database: Database = database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[settings.AUTH_ALGORITHM],
            )
            username = payload.get('sub')
            if username is None:
                raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)

        try:
            with _database.session() as session:
                user = _repo.get_by_username(session=session, username=username)
        except UserNotFoundException:
            raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)

        return UserResponseSchema.model_validate(user)

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserResponseSchema:
        return await AuthService._resolve_user_from_token(token=token)

    @staticmethod
    async def get_current_user_or_none(
        token: Annotated[str | None, Depends(optional_oauth2_scheme)],
    ) -> UserResponseSchema | None:
        if token is None:
            return None

        try:
            return await AuthService._resolve_user_from_token(token=token)
        except CredentialsException:
            return None
