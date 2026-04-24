from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends

from src.core.exceptions.database_exceptions import (
    LocationNotFoundException,
    CategoryNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    AuthorNotFoundException,
    LocationNotFoundByIdException,
    CategoryNotFoundByIdException,
)
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.list_posts import GetPostsUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.api.depends import (
    get_post_use_case,
    get_posts_use_case,
    create_post_use_case,
    update_post_use_case,
    delete_post_use_case,
)
from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)
from src.schemas.users import UserResponseSchema
from src.services.auth import AuthService

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[PostResponseSchema])
async def get_posts_list(
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: GetPostsUseCase = Depends(get_posts_use_case),
) -> list[PostResponseSchema]:
    return await use_case.execute()


@router.get('/get/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def get_post(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: GetPostUseCase = Depends(get_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(
    post: PostCreateSchema,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(data=post)
    except AuthorNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )


@router.put('/update/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def update_post(
    post_id: int,
    post: PostUpdateSchema,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(
            post_id=post_id,
            data=post,
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )


@router.delete('/delete/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
) -> dict:
    try:
        await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Публикация успешно удалена'}
