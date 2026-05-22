from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserResponseSchema


class GetUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[UserResponseSchema]:
        async with self._database.session() as session:
            users = await self._repo.get_all(session=session)
            users_data = [
                {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'date_joined': user.date_joined,
                }
                for user in users
            ]
        return [UserResponseSchema(**u) for u in users_data]
