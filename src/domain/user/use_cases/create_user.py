import bcrypt

from src.core.exceptions.domain_exceptions import UserUsernameOrEmailIsNotUniqueException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserCreateSchema, UserResponseSchema


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreateSchema) -> UserResponseSchema:
        with self._database.session() as session:
            existing = self._repo.get_by_username(
                session=session,
                username=data.username,
            )
            if existing is not None:
                raise UserUsernameOrEmailIsNotUniqueException.from_username(data.username)

            user = User(
                username=data.username,
                password=hash_password(data.password.get_secret_value()),
                email=data.email or '',
                first_name=data.first_name,
                last_name=data.last_name,
                is_active=True,
            )
            self._repo.create(session=session, user=user)

            return UserResponseSchema.model_validate(obj=user)
