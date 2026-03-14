from fastapi import APIRouter

from src.domain.location.use_cases.get_location import (
    CreateLocationUseCase,
    DeleteLocationUseCase,
    GetLocationUseCase,
    GetLocationsUseCase,
    UpdateLocationUseCase,
)
from src.schemas.locations import LocationCreateSchema, LocationUpdateSchema, LocationResponseSchema

router = APIRouter()


@router.get('/list')
async def get_locations_list() -> list[LocationResponseSchema]:
    use_case = GetLocationsUseCase()
    return await use_case.execute()


@router.get('/get/{location_id}')
async def get_location(location_id: int) -> LocationResponseSchema:
    use_case = GetLocationUseCase()
    return await use_case.execute(location_id=location_id)


@router.post('/create')
async def create_location(location: LocationCreateSchema) -> LocationResponseSchema:
    use_case = CreateLocationUseCase()
    return await use_case.execute(data=location)


@router.put('/update/{location_id}')
async def update_location(
    location_id: int, location: LocationUpdateSchema
) -> LocationResponseSchema:
    use_case = UpdateLocationUseCase()
    return await use_case.execute(location_id=location_id, data=location)


@router.delete('/delete/{location_id}')
async def delete_location(location_id: int) -> dict:
    use_case = DeleteLocationUseCase()
    await use_case.execute(location_id=location_id)
    return {'message': 'Местоположение успешно удалено'}
