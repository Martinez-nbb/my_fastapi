from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
)
from src.domain.user.use_cases.get_user import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    GetUsersUseCase,
    UpdateUserUseCase,
)
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)

user_router = APIRouter()


@user_router.get('/')
async def get_users() -> list[UserResponseSchema]:
    use_case = GetUsersUseCase()
    return await use_case.execute()


@user_router.get('/{user_id}')
async def get_user(user_id: int) -> UserResponseSchema:
    use_case = GetUserUseCase()
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@user_router.post('/')
async def create_user(data: UserCreateSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    try:
        return await use_case.execute(data=data)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )


@user_router.put('/{user_id}')
async def update_user(
    user_id: int,
    data: UserUpdateSchema,
) -> UserResponseSchema:
    use_case = UpdateUserUseCase()
    try:
        return await use_case.execute(
            user_id=user_id,
            data=data,
        )
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@user_router.delete('/{user_id}')
async def delete_user(user_id: int) -> dict:
    use_case = DeleteUserUseCase()
    try:
        await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': f'Пользователь с id={user_id} успешно удален'}
