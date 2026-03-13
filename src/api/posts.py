from fastapi import APIRouter, status

from src.domain.post.use_cases.get_post import (
    GetPostUseCase,
    GetPostsUseCase,
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
)
from src.schemas.posts import PostCreateSchema, PostUpdateSchema, PostResponseSchema

router = APIRouter()


@router.get(
    '/list',
    response_model=list[PostResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех публикаций",
    description="Возвращает список всех публикаций с вложенными объектами (author, location, category)",
)
async def get_posts_list() -> list[PostResponseSchema]:
    use_case = GetPostsUseCase()
    return await use_case.execute()


@router.get(
    '/get/{post_id}',
    response_model=PostResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить публикацию по ID",
    description="Возвращает публикацию по уникальному идентификатору с вложенными объектами",
)
async def get_post(post_id: int) -> PostResponseSchema:
    use_case = GetPostUseCase()
    return await use_case.execute(post_id=post_id)


@router.post(
    '/create',
    response_model=PostResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую публикацию",
    description="Создаёт новую публикацию с указанными данными",
)
async def create_post(post: PostCreateSchema) -> PostResponseSchema:
    use_case = CreatePostUseCase()
    return await use_case.execute(data=post)


@router.put(
    '/update/{post_id}',
    response_model=PostResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить публикацию",
    description="Обновляет существующую публикацию",
)
async def update_post(post_id: int, post: PostUpdateSchema) -> PostResponseSchema:
    use_case = UpdatePostUseCase()
    return await use_case.execute(post_id=post_id, data=post)


@router.delete(
    '/delete/{post_id}',
    status_code=status.HTTP_200_OK,
    summary="Удалить публикацию",
    description="Удаляет публикацию по уникальному идентификатору",
)
async def delete_post(post_id: int) -> dict:
    use_case = DeletePostUseCase()
    await use_case.execute(post_id=post_id)
    return {'message': 'Публикация успешно удалена'}
