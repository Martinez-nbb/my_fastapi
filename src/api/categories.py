from fastapi import APIRouter, status

from src.domain.category.use_cases.get_category import (
    GetCategoryUseCase,
    GetCategoriesUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)
from src.schemas.categories import CategoryCreateSchema, CategoryResponseSchema

router = APIRouter()


@router.get(
    '/list',
    response_model=list[CategoryResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех категорий",
    description="Возвращает список всех категорий, включая неопубликованные",
    response_description="Список категорий",
)
async def get_categories_list() -> list[CategoryResponseSchema]:
    use_case = GetCategoriesUseCase()
    return await use_case.execute()


@router.get(
    '/get/{category_id}',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить категорию по ID",
    description="Возвращает категорию по уникальному идентификатору",
    response_description="Объект категории",
)
async def get_category(category_id: int) -> CategoryResponseSchema:
    use_case = GetCategoryUseCase()
    return await use_case.execute(category_id=category_id)


@router.post(
    '/create',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую категорию",
    description="Создаёт новую категорию с указанными данными",
    response_description="Созданная категория",
)
async def create_category(category: CategoryCreateSchema) -> CategoryResponseSchema:
    use_case = CreateCategoryUseCase()
    return await use_case.execute(data=category)


@router.put(
    '/update/{category_id}',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить категорию",
    description="Обновляет существующую категорию",
    response_description="Обновлённая категория",
)
async def update_category(category_id: int, category: CategoryCreateSchema) -> CategoryResponseSchema:
    use_case = UpdateCategoryUseCase()
    return await use_case.execute(category_id=category_id, data=category)


@router.delete(
    '/delete/{category_id}',
    status_code=status.HTTP_200_OK,
    summary="Удалить категорию",
    description="Удаляет категорию по уникальному идентификатору",
    response_description="Сообщение об успешном удалении",
)
async def delete_category(category_id: int) -> dict:
    use_case = DeleteCategoryUseCase()
    await use_case.execute(category_id=category_id)
    return {'message': 'Категория успешно удалена'}
