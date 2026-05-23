import asyncio
import logging
from typing import Annotated, List

from fastapi import APIRouter, status, HTTPException, Depends, File as FileParam, UploadFile, Response
from sqlalchemy.exc import IntegrityError

from src.core.config import settings
from src.core.exceptions.database_exceptions import (
    CommentImageNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    CommentImageNotFoundByIdException,
    PostNotFoundByIdException,
    AuthorNotFoundException,
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
    ImageFolderNotWritableException,
)
from src.domain.comment.use_cases.add_comment_images import AddCommentImagesUseCase
from src.domain.comment.use_cases.delete_comment_image import DeleteCommentImageUseCase
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.list_comments import (
    GetCommentsUseCase,
    GetCommentsByPostUseCase,
)
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from src.domain.shared.async_file import async_read_file
from src.domain.shared.combine_images import combine_images_vertically
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comment_image import CommentImageRepository
from src.api.depends import (
    get_comment_use_case,
    get_comments_use_case,
    get_comments_by_post_use_case,
    create_comment_use_case,
    update_comment_use_case,
    delete_comment_use_case,
    add_comment_images_use_case,
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

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_list(
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetCommentsUseCase, Depends(get_comments_use_case)],
) -> list[CommentResponseSchema]:
    try:
        return await use_case.execute()
    except Exception as exc:
        logger.error(f"Ошибка получения списка комментариев: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/list/by_post/{post_id}', status_code=status.HTTP_200_OK, response_model=list[CommentResponseSchema])
async def get_comments_by_post(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetCommentsByPostUseCase, Depends(get_comments_by_post_use_case)],
) -> list[CommentResponseSchema]:
    try:
        return await use_case.execute(post_id=post_id)
    except Exception as exc:
        logger.error(f"Ошибка получения комментариев по посту: post_id={post_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
    except Exception as exc:
        logger.error(f"Ошибка при получении комментария: comment_id={comment_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
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
    except IntegrityError as exc:
        logger.error(f"IntegrityError при создании комментария: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных при создании комментария",
        )
    except Exception as exc:
        logger.error(f"Ошибка при создании комментария: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
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
    except IntegrityError as exc:
        logger.error(f"IntegrityError при обновлении комментария: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных при обновлении комментария",
        )
    except Exception as exc:
        logger.error(f"Ошибка при обновлении комментария: comment_id={comment_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
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
    except Exception as exc:
        logger.error(f"Ошибка при удалении комментария: comment_id={comment_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )
    return {'message': 'Комментарий успешно удален'}


@router.post('/images/{comment_id}', status_code=status.HTTP_201_CREATED, response_model=list[CommentImageSchema])
async def add_comment_images(
    comment_id: int,
    image: Annotated[List[UploadFile], FileParam(description='Изображения')],
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[AddCommentImagesUseCase, Depends(add_comment_images_use_case)],
) -> list[CommentImageSchema]:
    try:
        return await use_case.execute(comment_id=comment_id, images=image)
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
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    except ImageFolderNotWritableException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Необработанная ошибка при загрузке изображений: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.get('/{comment_id}/images', status_code=status.HTTP_200_OK, response_class=Response)
async def list_comment_images(
    comment_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
):
    image_folder = settings.IMAGE_FOLDER
    try:
        async with database.session() as session:
            images = await CommentImageRepository().get_by_comment(session=session, comment_id=comment_id)
    except Exception as exc:
        logger.error(f"Ошибка БД при получении изображений: comment_id={comment_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    file_paths = [img.file_path for img in images]
    if not file_paths:
        raise HTTPException(status_code=404, detail="Для этого комментария нет фото")

    try:
        loop = asyncio.get_running_loop()
        buf = await loop.run_in_executor(None, combine_images_vertically, file_paths, image_folder)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Нет доступных изображений для этого комментария")
    except Exception as exc:
        logger.error(f"Ошибка обработки изображений: comment_id={comment_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Ошибка обработки изображений")

    return Response(content=buf.read(), media_type="image/jpeg")


_MEDIA_TYPES = {
    "jpeg": "image/jpeg", "jpg": "image/jpeg",
    "png": "image/png", "gif": "image/gif", "webp": "image/webp",
}


@router.get('/image/{image_id}', status_code=status.HTTP_200_OK, response_class=Response)
async def get_comment_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
):
    try:
        async with database.session() as session:
            image = await CommentImageRepository().get(session=session, image_id=image_id)
    except CommentImageNotFoundException as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        logger.error(f"Ошибка БД при получении изображения: image_id={image_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    full_path = f"{settings.IMAGE_FOLDER}/{image.file_path}"
    try:
        content = await async_read_file(full_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image file not found on disk")

    ext = image.file_path.rsplit('.', 1)[-1] if '.' in image.file_path else ''
    media_type = _MEDIA_TYPES.get(ext, "image/jpeg")
    return Response(content=content, media_type=media_type)


@router.delete('/image/{image_id}', status_code=status.HTTP_200_OK)
async def delete_comment_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeleteCommentImageUseCase, Depends(delete_comment_image_use_case)],
) -> dict:
    try:
        await use_case.execute(image_id=image_id)
    except CommentImageNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при удалении изображения комментария: image_id={image_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )
    return {'message': f'Изображение комментария с id={image_id} успешно удалено'}
