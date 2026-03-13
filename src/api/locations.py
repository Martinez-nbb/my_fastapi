from fastapi import APIRouter, status

from src.domain.location.use_cases.get_location import (
    GetLocationUseCase,
    GetLocationsUseCase,
    CreateLocationUseCase,
    UpdateLocationUseCase,
    DeleteLocationUseCase,
)
from src.schemas.locations import LocationCreateSchema, LocationUpdateSchema, LocationResponseSchema

router = APIRouter()


@router.get(
    '/list',
    response_model=list[LocationResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех местоположений",
    description="Возвращает список всех местоположений",
)
async def get_locations_list() -> list[LocationResponseSchema]:
    use_case = GetLocationsUseCase()
    return await use_case.execute()


@router.get(
    '/get/{location_id}',
    response_model=LocationResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить местоположение по ID",
    description="Возвращает местоположение по уникальному идентификатору",
)
async def get_location(location_id: int) -> LocationResponseSchema:
    use_case = GetLocationUseCase()
    return await use_case.execute(location_id=location_id)


@router.post(
    '/create',
    response_model=LocationResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое местоположение",
    description="Создаёт новое местоположение с указанными данными",
)
async def create_location(location: LocationCreateSchema) -> LocationResponseSchema:
    use_case = CreateLocationUseCase()
    return await use_case.execute(data=location)


@router.put(
    '/update/{location_id}',
    response_model=LocationResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить местоположение",
    description="Обновляет существующее местоположение",
)
async def update_location(location_id: int, location: LocationUpdateSchema) -> LocationResponseSchema:
    use_case = UpdateLocationUseCase()
    return await use_case.execute(location_id=location_id, data=location)


@router.delete(
    '/delete/{location_id}',
    status_code=status.HTTP_200_OK,
    summary="Удалить местоположение",
    description="Удаляет местоположение по уникальному идентификатору",
)
async def delete_location(location_id: int) -> dict:
    use_case = DeleteLocationUseCase()
    await use_case.execute(location_id=location_id)
    return {'message': 'Местоположение успешно удалено'}
