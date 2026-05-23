import logging
from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends

from src.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
    LocationAlreadyExistsException,
)
from src.domain.location.use_cases.get_location import GetLocationUseCase
from src.domain.location.use_cases.list_locations import GetLocationsUseCase
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase
from src.api.depends import (
    get_location_use_case,
    get_locations_use_case,
    create_location_use_case,
    update_location_use_case,
    delete_location_use_case,
)
from src.schemas.locations import (
    LocationCreateSchema,
    LocationUpdateSchema,
    LocationResponseSchema,
)
from src.schemas.users import UserResponseSchema
from src.services.auth import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[LocationResponseSchema])
async def get_locations_list(
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetLocationsUseCase, Depends(get_locations_use_case)],
) -> list[LocationResponseSchema]:
    try:
        return await use_case.execute()
    except Exception as exc:
        logger.error(f"Ошибка получения списка местоположений: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/get/{location_id}', status_code=status.HTTP_200_OK, response_model=LocationResponseSchema)
async def get_location(
    location_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[GetLocationUseCase, Depends(get_location_use_case)],
) -> LocationResponseSchema:
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при получении местоположения: location_id={location_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=LocationResponseSchema)
async def create_location(
    location: LocationCreateSchema,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[CreateLocationUseCase, Depends(create_location_use_case)],
) -> LocationResponseSchema:
    try:
        return await use_case.execute(data=location)
    except LocationAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка создания местоположения: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put('/update/{location_id}', status_code=status.HTTP_200_OK, response_model=LocationResponseSchema)
async def update_location(
    location_id: int,
    location: LocationUpdateSchema,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[UpdateLocationUseCase, Depends(update_location_use_case)],
) -> LocationResponseSchema:
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
    except LocationAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при обновлении местоположения: location_id={location_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )


@router.delete('/delete/{location_id}', status_code=status.HTTP_200_OK)
async def delete_location(
    location_id: int,
    current_user: Annotated[UserResponseSchema, Depends(AuthService.get_current_user)],
    use_case: Annotated[DeleteLocationUseCase, Depends(delete_location_use_case)],
) -> dict:
    try:
        await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при удалении местоположения: location_id={location_id}, error={str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )
    return {'message': 'Местоположение успешно удалено'}
