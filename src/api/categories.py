from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugAlreadyExistsException,
)
from src.domain.category.use_cases.get_category import GetCategoryUseCase
from src.domain.category.use_cases.list_categories import GetCategoriesUseCase
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[CategoryResponseSchema])
async def get_categories_list() -> list[CategoryResponseSchema]:
    use_case = GetCategoriesUseCase()
    return await use_case.execute()


@router.get('/get/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseSchema)
async def get_category(category_id: int) -> CategoryResponseSchema:
    use_case = GetCategoryUseCase()
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CategoryResponseSchema)
async def create_category(
    category: CategoryCreateSchema,
) -> CategoryResponseSchema:
    use_case = CreateCategoryUseCase()
    try:
        return await use_case.execute(data=category)
    except CategorySlugAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )


@router.put('/update/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseSchema)
async def update_category(
    category_id: int,
    category: CategoryUpdateSchema,
) -> CategoryResponseSchema:
    use_case = UpdateCategoryUseCase()
    try:
        return await use_case.execute(
            category_id=category_id,
            data=category,
        )
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.delete('/delete/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(category_id: int) -> dict:
    use_case = DeleteCategoryUseCase()
    try:
        await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Категория успешно удалена'}
