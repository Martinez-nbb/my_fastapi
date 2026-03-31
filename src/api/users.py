from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserUsernameOrEmailIsNotUniqueException,
)
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)

user_router = APIRouter()


@user_router.get('/', status_code=status.HTTP_200_OK, response_model=list[UserResponseSchema])
async def get_users() -> list[UserResponseSchema]:
    use_case = GetUsersUseCase()
    return await use_case.execute()


@user_router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def get_user(user_id: int) -> UserResponseSchema:
    use_case = GetUserUseCase()
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(data: UserCreateSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    try:
        return await use_case.execute(data=data)
    except UserUsernameOrEmailIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )


@user_router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
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


@user_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
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
