from fastapi import APIRouter

from src.domain.post.use_cases.get_post import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostUseCase,
    GetPostsUseCase,
    UpdatePostUseCase,
)
from src.schemas.posts import PostCreateSchema, PostUpdateSchema, PostResponseSchema

router = APIRouter()


@router.get('/list')
async def get_posts_list() -> list[PostResponseSchema]:
    use_case = GetPostsUseCase()
    return await use_case.execute()


@router.get('/get/{post_id}')
async def get_post(post_id: int) -> PostResponseSchema:
    use_case = GetPostUseCase()
    return await use_case.execute(post_id=post_id)


@router.post('/create')
async def create_post(post: PostCreateSchema) -> PostResponseSchema:
    use_case = CreatePostUseCase()
    return await use_case.execute(data=post)


@router.put('/update/{post_id}')
async def update_post(post_id: int, post: PostUpdateSchema) -> PostResponseSchema:
    use_case = UpdatePostUseCase()
    return await use_case.execute(post_id=post_id, data=post)


@router.delete('/delete/{post_id}')
async def delete_post(post_id: int) -> dict:
    use_case = DeletePostUseCase()
    await use_case.execute(post_id=post_id)
    return {'message': 'Публикация успешно удалена'}
