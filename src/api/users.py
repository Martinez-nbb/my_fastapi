from fastapi import APIRouter, status

from src.domain.user.use_cases.get_user import (
    GetUserUseCase,
    GetUsersUseCase,
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from src.schemas.users import UserCreateSchema, UserResponseSchema

user_router = APIRouter()


@user_router.get(
    '/',
    response_model=list[UserResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех пользователей",
    description="Возвращает список всех пользователей системы",
)
async def get_users() -> list[UserResponseSchema]:
    use_case = GetUsersUseCase()
    return await use_case.execute()


@user_router.get(
    '/{user_id}',
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по ID",
    description="Возвращает пользователя по уникальному идентификатору",
)
async def get_user(user_id: int) -> UserResponseSchema:
    use_case = GetUserUseCase()
    return await use_case.execute(user_id=user_id)


@user_router.post(
    '/',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    description="Создаёт нового пользователя с указанными данными",
)
async def create_user(data: UserCreateSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    return await use_case.execute(data=data)


@user_router.put(
    '/{user_id}',
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя",
    description="Обновляет существующего пользователя",
)
async def update_user(user_id: int, data: UserCreateSchema) -> UserResponseSchema:
    use_case = UpdateUserUseCase()
    return await use_case.execute(user_id=user_id, data=data)


@user_router.delete(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    summary="Удалить пользователя",
    description="Удаляет пользователя по уникальному идентификатору",
)
async def delete_user(user_id: int) -> dict:
    use_case = DeleteUserUseCase()
    await use_case.execute(user_id=user_id)
    return {'message': f'Пользователь с id={user_id} успешно удален'}
