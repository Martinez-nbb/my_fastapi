from fastapi import APIRouter, status, HTTPException

from typing import List
from datetime import datetime

from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)
# APIRouter группирует все endpoints, связанные с категориями
# Префикс будет добавлен при подключении роутера в app.py
router = APIRouter(
    # prefix="/categories"  # Префикс добавляется при подключении в app.py
    # tags=["Categories"]   # Тег добавляется при подключении в app.py
)

categories_db: List[dict] = []

_categories_counter = 0
@router.get(
    "/list",
    response_model=List[CategoryResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех категорий",
    description="Возвращает список всех категорий, включая неопубликованные",
    response_description="Список категорий",
)
async def get_categories_list() -> List[dict]:
    
    return categories_db

@router.get(
    "/get/{category_id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить категорию по ID",
    description="Возвращает категорию по уникальному идентификатору",
    response_description="Объект категории",
)
async def get_category(category_id: int) -> dict:
    
    for category in categories_db:
        if category["id"] == category_id:
            return category
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Категория с id={category_id} не найдена",
    )

@router.post(
    "/create",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую категорию",
    description="Создаёт новую категорию с указанными данными",
    response_description="Созданная категория",
)
async def create_category(category: CategoryCreateSchema) -> dict:
    global _categories_counter
    _categories_counter += 1
    new_id = _categories_counter
    category_data = category.model_dump()
    category_data["id"] = new_id
    category_data["created_at"] = datetime.now()
    categories_db.append(category_data)
    return category_data


@router.put(
    "/update/{category_id}",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить категорию",
    description="Обновляет существующую категорию (partial update)",
    response_description="Обновлённая категория",
)
async def update_category(category_id: int, category: CategoryUpdateSchema) -> dict:
    
    for idx, cat in enumerate(categories_db):
        if cat["id"] == category_id:
            
            update_data = category.model_dump(exclude_unset=True)
            
            categories_db[idx].update(update_data)
            return categories_db[idx]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Категория с id={category_id} не найдена",
    )
@router.delete(
    "/delete/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить категорию",
    description="Удаляет категорию по уникальному идентификатору",
    response_description="Сообщение об успешном удалении",
)
async def delete_category(category_id: int) -> dict:
    
    for idx, cat in enumerate(categories_db):
        if cat["id"] == category_id:
            categories_db.pop(idx)
            return {"message": "Категория успешно удалена"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Категория с id={category_id} не найдена",
    )