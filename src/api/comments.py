from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
)
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.list_comments import (
    GetCommentsUseCase,
    GetCommentsByPostUseCase,
)
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from src.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentResponseSchema,
)

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_list() -> list[CommentResponseSchema]:
    use_case = GetCommentsUseCase()
    return await use_case.execute()


@router.get('/list/by_post/{post_id}', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_by_post(
    post_id: int,
) -> list[CommentResponseSchema]:
    use_case = GetCommentsByPostUseCase()
    return await use_case.execute(post_id=post_id)


@router.get('/get/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def get_comment(comment_id: int) -> CommentResponseSchema:
    use_case = GetCommentUseCase()
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CommentResponseSchema)
async def create_comment(
    comment: CommentCreateSchema,
    author_id: int,
) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    try:
        return await use_case.execute(
            data=comment,
            author_id=author_id,
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )


@router.put('/update/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def update_comment(
    comment_id: int,
    comment: CommentUpdateSchema,
) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    try:
        return await use_case.execute(
            comment_id=comment_id,
            data=comment,
        )
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.delete('/delete/{comment_id}', status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> dict:
    use_case = DeleteCommentUseCase()
    try:
        await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Комментарий успешно удален'}
