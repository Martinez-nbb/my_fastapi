from fastapi import APIRouter

from src.domain.category.use_cases.get_category import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    GetCategoriesUseCase,
    UpdateCategoryUseCase,
)
from src.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema, CategoryResponseSchema

router = APIRouter()


@router.get('/list')
async def get_categories_list() -> list[CategoryResponseSchema]:
    use_case = GetCategoriesUseCase()
    return await use_case.execute()


@router.get('/get/{category_id}')
async def get_category(category_id: int) -> CategoryResponseSchema:
    use_case = GetCategoryUseCase()
    return await use_case.execute(category_id=category_id)


@router.post('/create')
async def create_category(category: CategoryCreateSchema) -> CategoryResponseSchema:
    use_case = CreateCategoryUseCase()
    return await use_case.execute(data=category)


@router.put('/update/{category_id}')
async def update_category(
    category_id: int, category: CategoryUpdateSchema
) -> CategoryResponseSchema:
    use_case = UpdateCategoryUseCase()
    return await use_case.execute(category_id=category_id, data=category)


@router.delete('/delete/{category_id}')
async def delete_category(category_id: int) -> dict:
    use_case = DeleteCategoryUseCase()
    await use_case.execute(category_id=category_id)
    return {'message': 'Категория успешно удалена'}
