from fastapi import APIRouter

from src.domain.user.use_cases.get_user import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    GetUsersUseCase,
    UpdateUserUseCase,
)
from src.schemas.users import UserCreateSchema, UserUpdateSchema, UserResponseSchema

user_router = APIRouter()


@user_router.get('/')
async def get_users() -> list[UserResponseSchema]:
    use_case = GetUsersUseCase()
    return await use_case.execute()


@user_router.get('/{user_id}')
async def get_user(user_id: int) -> UserResponseSchema:
    use_case = GetUserUseCase()
    return await use_case.execute(user_id=user_id)


@user_router.post('/')
async def create_user(data: UserCreateSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    return await use_case.execute(data=data)


@user_router.put('/{user_id}')
async def update_user(user_id: int, data: UserUpdateSchema) -> UserResponseSchema:
    use_case = UpdateUserUseCase()
    return await use_case.execute(user_id=user_id, data=data)


@user_router.delete('/{user_id}')
async def delete_user(user_id: int) -> dict:
    use_case = DeleteUserUseCase()
    await use_case.execute(user_id=user_id)
    return {'message': f'Пользователь с id={user_id} успешно удален'}
