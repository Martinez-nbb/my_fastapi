from fastapi import APIRouter, status, HTTPException

from src.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
)
from src.domain.location.use_cases.get_location import GetLocationUseCase
from src.domain.location.use_cases.list_locations import GetLocationsUseCase
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase
from src.schemas.locations import (
    LocationCreateSchema,
    LocationUpdateSchema,
    LocationResponseSchema,
)

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[LocationResponseSchema])
async def get_locations_list() -> list[LocationResponseSchema]:
    use_case = GetLocationsUseCase()
    return await use_case.execute()


@router.get('/get/{location_id}', status_code=status.HTTP_200_OK, response_model=LocationResponseSchema)
async def get_location(location_id: int) -> LocationResponseSchema:
    use_case = GetLocationUseCase()
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=LocationResponseSchema)
async def create_location(
    location: LocationCreateSchema,
) -> LocationResponseSchema:
    use_case = CreateLocationUseCase()
    return await use_case.execute(data=location)


@router.put('/update/{location_id}', status_code=status.HTTP_200_OK, response_model=LocationResponseSchema)
async def update_location(
    location_id: int,
    location: LocationUpdateSchema,
) -> LocationResponseSchema:
    use_case = UpdateLocationUseCase()
    try:
        return await use_case.execute(
            location_id=location_id,
            data=location,
        )
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@router.delete('/delete/{location_id}', status_code=status.HTTP_200_OK)
async def delete_location(location_id: int) -> dict:
    use_case = DeleteLocationUseCase()
    try:
        await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    return {'message': 'Местоположение успешно удалено'}
