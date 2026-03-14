from fastapi import APIRouter

from src.domain.comment.use_cases.get_comment import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    GetCommentUseCase,
    GetCommentsByPostUseCase,
    GetCommentsUseCase,
    UpdateCommentUseCase,
)
from src.schemas.comments import CommentCreateSchema, CommentUpdateSchema, CommentResponseSchema

router = APIRouter()


@router.get('/list')
async def get_comments_list() -> list[CommentResponseSchema]:
    use_case = GetCommentsUseCase()
    return await use_case.execute()


@router.get('/list/by_post/{post_id}')
async def get_comments_by_post(post_id: int) -> list[CommentResponseSchema]:
    use_case = GetCommentsByPostUseCase()
    return await use_case.execute(post_id=post_id)


@router.get('/get/{comment_id}')
async def get_comment(comment_id: int) -> CommentResponseSchema:
    use_case = GetCommentUseCase()
    return await use_case.execute(comment_id=comment_id)


@router.post('/create')
async def create_comment(comment: CommentCreateSchema) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    return await use_case.execute(data=comment)


@router.put('/update/{comment_id}')
async def update_comment(
    comment_id: int, comment: CommentUpdateSchema
) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    return await use_case.execute(comment_id=comment_id, data=comment)


@router.delete('/delete/{comment_id}')
async def delete_comment(comment_id: int) -> dict:
    use_case = DeleteCommentUseCase()
    await use_case.execute(comment_id=comment_id)
    return {'message': 'Комментарий успешно удален'}
