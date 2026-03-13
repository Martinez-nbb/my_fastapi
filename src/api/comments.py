from fastapi import APIRouter, status

from src.domain.comment.use_cases.get_comment import (
    GetCommentUseCase,
    GetCommentsUseCase,
    GetCommentsByPostUseCase,
    CreateCommentUseCase,
    UpdateCommentUseCase,
    DeleteCommentUseCase,
)
from src.schemas.comments import CommentCreateSchema, CommentUpdateSchema, CommentResponseSchema

router = APIRouter()


@router.get(
    '/list',
    response_model=list[CommentResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех комментариев",
    description="Возвращает список всех комментариев",
)
async def get_comments_list() -> list[CommentResponseSchema]:
    use_case = GetCommentsUseCase()
    return await use_case.execute()


@router.get(
    '/list/by_post/{post_id}',
    response_model=list[CommentResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить комментарии к публикации",
    description="Возвращает все комментарии к конкретной публикации, отсортированные по дате создания",
)
async def get_comments_by_post(post_id: int) -> list[CommentResponseSchema]:
    use_case = GetCommentsByPostUseCase()
    return await use_case.execute(post_id=post_id)


@router.get(
    '/get/{comment_id}',
    response_model=CommentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить комментарий по ID",
    description="Возвращает комментарий по уникальному идентификатору",
)
async def get_comment(comment_id: int) -> CommentResponseSchema:
    use_case = GetCommentUseCase()
    return await use_case.execute(comment_id=comment_id)


@router.post(
    '/create',
    response_model=CommentResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый комментарий",
    description="Создаёт новый комментарий к публикации",
)
async def create_comment(comment: CommentCreateSchema) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    return await use_case.execute(data=comment)


@router.put(
    '/update/{comment_id}',
    response_model=CommentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить комментарий",
    description="Обновляет существующий комментарий",
)
async def update_comment(comment_id: int, comment: CommentUpdateSchema) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    return await use_case.execute(comment_id=comment_id, data=comment)


@router.delete(
    '/delete/{comment_id}',
    status_code=status.HTTP_200_OK,
    summary="Удалить комментарий",
    description="Удаляет комментарий по уникальному идентификатору",
)
async def delete_comment(comment_id: int) -> dict:
    use_case = DeleteCommentUseCase()
    await use_case.execute(comment_id=comment_id)
    return {'message': 'Комментарий успешно удален'}
