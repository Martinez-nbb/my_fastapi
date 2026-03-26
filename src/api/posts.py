from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.list_posts import GetPostsUseCase
from src.domain.post.use_cases.post_commands import (
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
)
from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)

router = APIRouter()


@router.get('/list')
async def get_posts_list() -> list[PostResponseSchema]:
    use_case = GetPostsUseCase()
    return await use_case.execute()


@router.get('/get/{post_id}')
async def get_post(post_id: int) -> PostResponseSchema:
    use_case = GetPostUseCase()
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreateSchema) -> PostResponseSchema:
    use_case = CreatePostUseCase()
    try:
        return await use_case.execute(data=post)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )


@router.put('/update/{post_id}')
async def update_post(
    post_id: int,
    post: PostUpdateSchema,
) -> PostResponseSchema:
    use_case = UpdatePostUseCase()
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


@router.delete('/delete/{post_id}')
async def delete_post(post_id: int) -> dict:
    use_case = DeletePostUseCase()
    try:
        await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Публикация успешно удалена'}
