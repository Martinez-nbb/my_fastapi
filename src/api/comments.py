from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends, File as FileParam, UploadFile

from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.database_exceptions import (
    PostImageNotFoundException,
    CommentImageNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    AuthorNotFoundException,
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
)
from src.domain.comment.use_cases.add_comment_image import AddCommentImageUseCase
from src.domain.comment.use_cases.list_comment_images import ListCommentImagesUseCase
from src.domain.comment.use_cases.delete_comment_image import DeleteCommentImageUseCase
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
    add_comment_image_use_case,
    list_comment_images_use_case,
    delete_comment_image_use_case,
)
from src.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentResponseSchema,
    CommentImageSchema,
)
from src.schemas.users import UserResponseSchema
from src.services.auth import AuthService

router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_list(
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetCommentsUseCase, Depends(get_comments_use_case)],
) -> list[CommentResponseSchema]:
    return await use_case.execute()


@router.get('/list/by_post/{post_id}', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_by_post(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetCommentsByPostUseCase, Depends(get_comments_by_post_use_case)],
) -> list[CommentResponseSchema]:
    return await use_case.execute(post_id=post_id)


@router.get('/get/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def get_comment(
    comment_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetCommentUseCase, Depends(get_comment_use_case)],
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
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[CreateCommentUseCase, Depends(create_comment_use_case)],
) -> CommentResponseSchema:
    try:
        return await use_case.execute(
            data=comment,
            author_id=current_user.id,
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
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[UpdateCommentUseCase, Depends(update_comment_use_case)],
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
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeleteCommentUseCase, Depends(delete_comment_use_case)],
) -> dict:
    try:
        await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Комментарий успешно удален'}


@router.post('/image/{comment_id}', status_code=status.HTTP_201_CREATED, response_model=CommentImageSchema)
async def add_comment_image(
    comment_id: int,
    image: Annotated[UploadFile, FileParam(description='Изображение')],
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[AddCommentImageUseCase, Depends(add_comment_image_use_case)],
) -> CommentImageSchema:
    try:
        return await use_case.execute(comment_id=comment_id, image=image)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except UploadFileIsNotImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )
    except ImageFileReadException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except ImageFileSaveException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
    except ImageFolderNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Необработанная ошибка при загрузке изображения: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.get('/{comment_id}/images', status_code=status.HTTP_200_OK, response_model=list[CommentImageSchema])
async def list_comment_images(
    comment_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[ListCommentImagesUseCase, Depends(list_comment_images_use_case)],
) -> list[CommentImageSchema]:
    return await use_case.execute(comment_id=comment_id)


@router.delete('/image/{image_id}', status_code=status.HTTP_200_OK)
async def delete_comment_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeleteCommentImageUseCase, Depends(delete_comment_image_use_case)],
) -> dict:
    try:
        await use_case.execute(image_id=image_id)
    except CommentImageNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc._detail,
        )
    return {'message': 'Изображение успешно удалено'}
