from fastapi import APIRouter, status, HTTPException

from typing import List
from datetime import datetime

from src.schemas.locations import (
    LocationCreateSchema,
    LocationUpdateSchema,
    LocationResponseSchema,
)
router = APIRouter(
    # prefix="/locations"  # Добавляется при подключении в app.py
    # tags=["Locations"]   # Добавляется при подключении в app.py
)
locations_db: List[dict] = []

_locations_counter = 0
@router.get(
    "/list",
    response_model=List[LocationResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех местоположений",
    description="Возвращает список всех местоположений",
)
async def get_locations_list() -> List[dict]:
    
    return locations_db
@router.get(
    "/get/{location_id}",
    response_model=LocationResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить местоположение по ID",
    description="Возвращает местоположение по уникальному идентификатору",
)
async def get_location(location_id: int) -> dict:
    for location in locations_db:
        if location["id"] == location_id:
            return location
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Местоположение с id={location_id} не найдено",
    )
@router.post(
    "/create",
    response_model=LocationResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое местоположение",
    description="Создаёт новое местоположение с указанными данными",
)
async def create_location(location: LocationCreateSchema) -> dict:
    global _locations_counter
    _locations_counter += 1
    new_id = _locations_counter
    location_data = location.model_dump()
    location_data["id"] = new_id
    location_data["created_at"] = datetime.now()
    locations_db.append(location_data)
    return location_data


@router.put(
    "/update/{location_id}",
    response_model=LocationResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить местоположение",
    description="Обновляет существующее местоположение (partial update)",
)
async def update_location(location_id: int, location: LocationUpdateSchema) -> dict:
    for idx, loc in enumerate(locations_db):
        if loc["id"] == location_id:
            update_data = location.model_dump(exclude_unset=True)
            
            locations_db[idx].update(update_data)
            
            return locations_db[idx]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Местоположение с id={location_id} не найдено",
    )
@router.delete(
    "/delete/{location_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить местоположение",
    description="Удаляет местоположение по уникальному идентификатору",
)
async def delete_location(location_id: int) -> dict:
    for idx, loc in enumerate(locations_db):
        if loc["id"] == location_id:
            locations_db.pop(idx)
            return {"message": "Местоположение успешно удалено"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Местоположение с id={location_id} не найдено",
    )