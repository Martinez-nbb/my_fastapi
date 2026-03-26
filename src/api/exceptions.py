from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions.database_exceptions import BaseDatabaseException
from src.core.exceptions.domain_exceptions import BaseDomainException


def register_exception_handlers(app: FastAPI) -> None:
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        errors = []
        for error in exc.errors():
            field = ".".join(str(x) for x in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"],
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "detail": "Ошибка валидации данных",
                "errors": errors,
            },
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "detail": "Ошибка валидации данных",
                "errors": [
                    {"field": ".".join(str(x) for x in err["loc"]), "message": err["msg"]}
                    for err in exc.errors()
                ],
            },
        )

    @app.exception_handler(BaseDomainException)
    async def domain_exception_handler(
        request: Request,
        exc: BaseDomainException,
    ) -> JSONResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        
        # Определяем статус код по типу исключения
        exception_name = exc.__class__.__name__
        if "NotFound" in exception_name:
            status_code = status.HTTP_404_NOT_FOUND
        elif "AlreadyExists" in exception_name or "Unique" in exception_name:
            status_code = status.HTTP_409_CONFLICT
        elif "NotUnique" in exception_name:
            status_code = status.HTTP_409_CONFLICT

        return JSONResponse(
            status_code=status_code,
            content={
                "error": exc.error_type,
                "detail": exc.get_detail(),
            },
        )

    @app.exception_handler(BaseDatabaseException)
    async def database_exception_handler(
        request: Request,
        exc: BaseDatabaseException,
    ) -> JSONResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        
        exception_name = exc.__class__.__name__
        if "NotFound" in exception_name:
            status_code = status.HTTP_404_NOT_FOUND
        elif "AlreadyExists" in exception_name:
            status_code = status.HTTP_409_CONFLICT
        elif "Integrity" in exception_name:
            status_code = status.HTTP_409_CONFLICT
        elif "Connection" in exception_name:
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        elif "Timeout" in exception_name:
            status_code = status.HTTP_504_GATEWAY_TIMEOUT

        return JSONResponse(
            status_code=status_code,
            content={
                "error": exc.error_type,
                "detail": exc.get_detail(),
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "DatabaseError",
                "detail": "Ошибка базы данных",
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "detail": "Внутренняя ошибка сервера",
            },
        )
