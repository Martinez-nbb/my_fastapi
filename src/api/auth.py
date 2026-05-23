import logging

from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.auth import Token, RefreshTokenRequest
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.domain.auth.use_cases.create_refresh_token import CreateRefreshTokenUseCase
from src.domain.auth.use_cases.refresh_access_token import RefreshAccessTokenUseCase
from src.core.exceptions.domain_exceptions import (
    InvalidCredentialsException,
    UserNotFoundByUsernameException,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[AuthenticateUserUseCase, Depends(AuthenticateUserUseCase)],
    create_token_use_case: Annotated[CreateAccessTokenUseCase, Depends(CreateAccessTokenUseCase)],
    create_refresh_uc: Annotated[CreateRefreshTokenUseCase, Depends(CreateRefreshTokenUseCase)],
) -> Token:
    try:
        user = await auth_use_case.execute(
            username=form_data.username, password=form_data.password
        )
    except InvalidCredentialsException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при аутентификации: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )

    try:
        access_token = await create_token_use_case.execute(username=user.username)
        refresh_token = await create_refresh_uc.execute(user_id=user.id)
    except Exception as exc:
        logger.error(f"Ошибка при создании токенов: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )


@router.post('/refresh', response_model=Token)
async def refresh_access_token(
    body: RefreshTokenRequest,
    refresh_uc: Annotated[RefreshAccessTokenUseCase, Depends(RefreshAccessTokenUseCase)],
) -> Token:
    try:
        access_token, refresh_token = await refresh_uc.execute(
            refresh_token=body.refresh_token,
        )
    except InvalidCredentialsException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
        )
    except Exception as exc:
        logger.error(f"Ошибка при обновлении токена: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )
