from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends

from src.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserUsernameAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserUsernameOrEmailIsNotUniqueException,
)
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase
from src.api.depends import (
    get_user_use_case,
    get_users_use_case,
    create_user_use_case,
    update_user_use_case,
    delete_user_use_case,
)
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)
from src.services.auth import AuthService

user_router = APIRouter()


@user_router.get('/', status_code=status.HTTP_200_OK, response_model=list[UserResponseSchema])
async def get_users(
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: GetUsersUseCase = Depends(get_users_use_case),
) -> list[UserResponseSchema]:
    return await use_case.execute()


@user_router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def get_user(
    user_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: GetUserUseCase = Depends(get_user_use_case),
) -> UserResponseSchema:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(
    data: UserCreateSchema,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> UserResponseSchema:
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
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: UpdateUserUseCase = Depends(update_user_use_case),
) -> UserResponseSchema:
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
    except UserEmailAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Пользователь с email "{data.email}" уже существует',
        )
    except UserUsernameAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Пользователь с именем "{data.username}" уже существует',
        )


@user_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: DeleteUserUseCase = Depends(delete_user_use_case),
) -> dict:
    try:
        await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': f'Пользователь с id={user_id} успешно удален'}
