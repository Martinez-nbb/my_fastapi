import asyncio
import logging
from typing import Annotated, List

from fastapi import APIRouter, status, HTTPException, Depends, File as FileParam, UploadFile, Response
from sqlalchemy.exc import IntegrityError

from src.core.config import settings
from src.domain.shared.async_file import async_read_file
from src.domain.shared.combine_images import combine_images_vertically
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.post_image import PostImageRepository

from src.core.exceptions.database_exceptions import (
    PostImageNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    PostImageNotFoundByIdException,
    AuthorNotFoundException,
    LocationNotFoundByIdException,
    CategoryNotFoundByIdException,
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
    ImageFolderNotWritableException,
)
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.list_posts import GetPostsUseCase
from src.domain.post.use_cases.list_posts_by_user import GetPostsByUserUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.domain.post.use_cases.add_post_images import AddPostImagesUseCase
from src.domain.post.use_cases.delete_post_image import DeletePostImageUseCase
from src.api.depends import (
    get_post_use_case,
    get_posts_use_case,
    get_posts_by_user_use_case,
    create_post_use_case,
    update_post_use_case,
    delete_post_use_case,
    add_post_images_use_case,
    delete_post_image_use_case,
)
from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
    PostImageSchema,
)
from src.schemas.users import UserResponseSchema
from src.services.auth import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[PostResponseSchema])
async def get_posts_list(
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetPostsUseCase, Depends(get_posts_use_case)],
) -> list[PostResponseSchema]:
    try:
        return await use_case.execute()
    except Exception as exc:
        logger.error(f"Ошибка получения списка постов: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/by_user/{user_id}', status_code=status.HTTP_200_OK, response_model=list[PostResponseSchema])
async def get_posts_by_user(
    user_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetPostsByUserUseCase, Depends(get_posts_by_user_use_case)],
) -> list[PostResponseSchema]:
    try:
        return await use_case.execute(user_id=user_id)
    except Exception as exc:
        logger.error(f"Ошибка получения постов пользователя: user_id={user_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/get/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def get_post(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetPostUseCase, Depends(get_post_use_case)],
) -> PostResponseSchema:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при получении поста: post_id={post_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(
    post: PostCreateSchema,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[CreatePostUseCase, Depends(create_post_use_case)],
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
    except IntegrityError as exc:
        logger.error(f"IntegrityError при создании поста: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных при создании публикации",
        )
    except Exception as exc:
        logger.error(f"Ошибка при создании поста: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.put('/update/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def update_post(
    post_id: int,
    post: PostUpdateSchema,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[UpdatePostUseCase, Depends(update_post_use_case)],
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
    except IntegrityError as exc:
        logger.error(f"IntegrityError при обновлении поста: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных при обновлении публикации",
        )
    except Exception as exc:
        logger.error(f"Ошибка при обновлении поста: post_id={post_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.delete('/delete/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeletePostUseCase, Depends(delete_post_use_case)],
) -> dict:
    try:
        await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при удалении поста: post_id={post_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )
    return {'message': 'Публикация успешно удалена'}


@router.post('/images/{post_id}', status_code=status.HTTP_201_CREATED, response_model=list[PostImageSchema])
async def add_post_images(
    post_id: int,
    image: Annotated[List[UploadFile], FileParam(description='Изображения (JPEG/PNG)')],
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[AddPostImagesUseCase, Depends(add_post_images_use_case)],
) -> list[PostImageSchema]:
    try:
        return await use_case.execute(post_id=post_id, images=image)
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
    except PostNotFoundByIdException as exc:
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


@router.get('/{post_id}/images', status_code=status.HTTP_200_OK, response_class=Response)
async def list_post_images(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
):
    image_folder = settings.IMAGE_FOLDER
    try:
        async with database.session() as session:
            images = await PostImageRepository().get_by_post(session=session, post_id=post_id)
    except Exception as exc:
        logger.error(f"Ошибка БД при получении изображений: post_id={post_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    file_paths = [img.file_path for img in images]
    if not file_paths:
        raise HTTPException(status_code=404, detail="Для этого поста нет фото")

    try:
        loop = asyncio.get_running_loop()
        buf = await loop.run_in_executor(None, combine_images_vertically, file_paths, image_folder)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Нет доступных изображений для этого поста")
    except Exception as exc:
        logger.error(f"Ошибка обработки изображений: post_id={post_id}, error={str(exc)}")
        raise HTTPException(status_code=500, detail="Ошибка обработки изображений")

    return Response(content=buf.read(), media_type="image/jpeg")


_MEDIA_TYPES = {
    "jpeg": "image/jpeg", "jpg": "image/jpeg",
    "png": "image/png", "gif": "image/gif", "webp": "image/webp",
}


@router.get('/image/{image_id}', status_code=status.HTTP_200_OK, response_class=Response)
async def get_post_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
):
    try:
        async with database.session() as session:
            image = await PostImageRepository().get(session=session, image_id=image_id)
    except PostImageNotFoundException as exc:
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
async def delete_post_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeletePostImageUseCase, Depends(delete_post_image_use_case)],
) -> dict:
    try:
        await use_case.execute(image_id=image_id)
    except PostImageNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при удалении изображения: image_id={image_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )
    return {'message': f'Изображение с id={image_id} успешно удалено'}
