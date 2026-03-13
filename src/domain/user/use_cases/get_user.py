from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserCreateSchema, UserResponseSchema


class GetUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponseSchema:
        with self._database.session() as session:
            user = self._repo.get(session=session, user_id=user_id)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь с id={user_id} не найден'
                )

        return UserResponseSchema.model_validate(obj=user)


class GetUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[UserResponseSchema]:
        with self._database.session() as session:
            users = self._repo.get_all(session=session)

        return [UserResponseSchema.model_validate(obj=user) for user in users]


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreateSchema) -> UserResponseSchema:
        with self._database.session() as session:
            # Проверка на существующего пользователя
            existing = self._repo.get_by_username(session=session, username=data.username)
            if existing:
                raise HTTPException(
                    status_code=400, detail=f'Пользователь "{data.username}" уже существует'
                )

            user = User(
                username=data.username,
                password=data.password,
                email=data.email,
                first_name='',
                last_name='',
                is_active=True,
            )
            self._repo.create(session=session, user=user)

        return UserResponseSchema.model_validate(obj=user)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, data: UserCreateSchema) -> UserResponseSchema:
        with self._database.session() as session:
            user = self._repo.get(session=session, user_id=user_id)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь с id={user_id} не найден'
                )

            self._repo.update(session=session, user=user, data=data)

        return UserResponseSchema.model_validate(obj=user)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int):
        with self._database.session() as session:
            user = self._repo.get(session=session, user_id=user_id)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь с id={user_id} не найден'
                )

            self._repo.delete(session=session, user=user)
