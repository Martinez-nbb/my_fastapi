from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserUpdateSchema, UserResponseSchema


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        user_id: int,
        data: UserUpdateSchema,
    ) -> UserResponseSchema:
        with self._database.session() as session:
            try:
                user = self._repo.get(
                    session=session,
                    user_id=user_id,
                )
            except UserNotFoundException:
                raise UserNotFoundByIdException(id=user_id)

            self._repo.update(
                session=session,
                user=user,
                data=data,
            )

            return UserResponseSchema.model_validate(obj=user)
