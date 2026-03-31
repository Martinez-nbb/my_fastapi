from fastapi import APIRouter, status, HTTPException, Depends

from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    AuthorNotFoundException,
)
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.list_comments import (
    GetCommentsUseCase,
    GetCommentsByPostUseCase,
)
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from src.api.depends import (
    get_comment_use_case,
    get_comments_use_case,
    get_comments_by_post_use_case,
    create_comment_use_case,
    update_comment_use_case,
    delete_comment_use_case,
)
from src.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentResponseSchema,
)

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_list(
    use_case: GetCommentsUseCase = Depends(get_comments_use_case),
) -> list[CommentResponseSchema]:
    return await use_case.execute()


@router.get('/list/by_post/{post_id}', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_by_post(
    post_id: int,
    use_case: GetCommentsByPostUseCase = Depends(get_comments_by_post_use_case),
) -> list[CommentResponseSchema]:
    return await use_case.execute(post_id=post_id)


@router.get('/get/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def get_comment(
    comment_id: int,
    use_case: GetCommentUseCase = Depends(get_comment_use_case),
) -> CommentResponseSchema:
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
    use_case: CreateCommentUseCase = Depends(create_comment_use_case),
) -> CommentResponseSchema:
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
    except AuthorNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )


@router.put('/update/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def update_comment(
    comment_id: int,
    comment: CommentUpdateSchema,
    use_case: UpdateCommentUseCase = Depends(update_comment_use_case),
) -> CommentResponseSchema:
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
async def delete_comment(
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends(delete_comment_use_case),
) -> dict:
    try:
        await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Комментарий успешно удален'}
