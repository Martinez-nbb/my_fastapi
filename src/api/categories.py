from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
)
from src.domain.category.use_cases.get_category import GetCategoryUseCase
from src.domain.category.use_cases.list_categories import GetCategoriesUseCase
from src.domain.category.use_cases.category_commands import (
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter()


@router.get('/list')
async def get_categories_list() -> list[CategoryResponseSchema]:
    use_case = GetCategoriesUseCase()
    return await use_case.execute()


@router.get('/get/{category_id}')
async def get_category(category_id: int) -> CategoryResponseSchema:
    use_case = GetCategoryUseCase()
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.post('/create')
async def create_category(
    category: CategoryCreateSchema,
) -> CategoryResponseSchema:
    use_case = CreateCategoryUseCase()
    return await use_case.execute(data=category)


@router.put('/update/{category_id}')
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


@router.delete('/delete/{category_id}')
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
