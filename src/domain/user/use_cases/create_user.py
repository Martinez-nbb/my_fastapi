from src.core.exceptions.database_exceptions import (
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import UserUsernameOrEmailIsNotUniqueException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserCreateSchema, UserResponseSchema


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreateSchema) -> UserResponseSchema:
        with self._database.session() as session:
            try:
                user = self._repo.create(session=session, data=data)
            except UserUsernameAlreadyExistsException:
                raise UserUsernameOrEmailIsNotUniqueException.from_username(
                    username=data.username
                )
            except UserEmailAlreadyExistsException:
                raise UserUsernameOrEmailIsNotUniqueException.from_email(
                    email=data.email
                )

            return UserResponseSchema.model_validate(obj=user)
