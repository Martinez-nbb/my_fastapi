from fastapi import APIRouter, status, HTTPException, Depends

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugAlreadyExistsException,
)
from src.domain.category.use_cases.get_category import GetCategoryUseCase
from src.domain.category.use_cases.list_categories import GetCategoriesUseCase
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase
from src.api.depends import (
    get_category_use_case,
    get_categories_use_case,
    create_category_use_case,
    update_category_use_case,
    delete_category_use_case,
)
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[CategoryResponseSchema])
async def get_categories_list(
    use_case: GetCategoriesUseCase = Depends(get_categories_use_case),
) -> list[CategoryResponseSchema]:
    return await use_case.execute()


@router.get('/get/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponseSchema)
async def get_category(
    category_id: int,
    use_case: GetCategoryUseCase = Depends(get_category_use_case),
) -> CategoryResponseSchema:
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
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponseSchema:
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
    use_case: UpdateCategoryUseCase = Depends(update_category_use_case),
) -> CategoryResponseSchema:
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
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
) -> dict:
    try:
        await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Категория успешно удалена'}
