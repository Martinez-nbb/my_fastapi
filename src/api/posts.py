import logging
from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends, File as FileParam, UploadFile
from fastapi.responses import FileResponse

from src.core.exceptions.database_exceptions import (
    LocationNotFoundException,
    CategoryNotFoundException,
    PostNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    AuthorNotFoundException,
    LocationNotFoundByIdException,
    CategoryNotFoundByIdException,
    UploadFileIsNotImageException,
    ImageFileReadException,
    ImageFileSaveException,
    ImageFolderNotFoundException,
)
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.list_posts import GetPostsUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.domain.post.use_cases.add_post_image import AddPostImageUseCase
from src.domain.post.use_cases.get_post_image import GetPostImageUseCase
from src.domain.post.use_cases.list_post_images import ListPostImagesUseCase
from src.domain.post.use_cases.delete_post_image import DeletePostImageUseCase
from src.api.depends import (
    get_post_use_case,
    get_posts_use_case,
    create_post_use_case,
    update_post_use_case,
    delete_post_use_case,
    add_post_image_use_case,
    get_post_image_use_case,
    list_post_images_use_case,
    delete_post_image_use_case,
)
from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
    PostImageSchema,
    PostImageResponse,
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
    return await use_case.execute()


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
    return {'message': 'Публикация успешно удалена'}


@router.post('/image/{post_id}', status_code=status.HTTP_201_CREATED, response_model=PostImageSchema)
async def add_post_image(
    post_id: int,
    image: Annotated[UploadFile, FileParam(description='Изображение (JPEG)')],
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[AddPostImageUseCase, Depends(add_post_image_use_case)],
) -> PostImageSchema:
    try:
        return await use_case.execute(post_id=post_id, image=image)
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
    except PostNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc._detail,
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


@router.get('/{post_id}/images', status_code=status.HTTP_200_OK, response_model=list[PostImageSchema])
async def list_post_images(
    post_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[ListPostImagesUseCase, Depends(list_post_images_use_case)],
) -> list[PostImageSchema]:
    return await use_case.execute(post_id=post_id)


@router.get('/image/{image_id}')
async def get_post_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetPostImageUseCase, Depends(get_post_image_use_case)],
) -> FileResponse:
    try:
        return await use_case.execute(image_id=image_id)
    except PostNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc._detail,
        )


@router.delete('/image/{image_id}', status_code=status.HTTP_200_OK)
async def delete_post_image(
    image_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeletePostImageUseCase, Depends(delete_post_image_use_case)],
) -> dict:
    try:
        await use_case.execute(image_id=image_id)
    except PostNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc._detail,
        )
    return {'message': 'Изображение успешно удалено'}
