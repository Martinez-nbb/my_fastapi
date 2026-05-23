from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.core.logging import setup_logging, get_logger
from src.api.users import user_router, public_user_router
from src.api.categories import router as categories_router
from src.api.locations import router as locations_router
from src.api.posts import router as posts_router
from src.api.comments import router as comments_router
from src.api.auth import router as auth_router

setup_logging()
logger = get_logger(__name__)


async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


def _error_response(status_code: int, detail: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": detail})

def create_app() -> FastAPI:
    app = FastAPI(root_path='/api/v1')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.middleware('http')(log_requests)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception: {request.method} {request.url}")
        return _error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера",
        )

    app.include_router(
        auth_router,
        prefix='/auth',
        tags=['Auth'],
    )
    app.include_router(
        public_user_router,
        prefix='/users',
        tags=['Users (public)'],
    )
    app.include_router(
        user_router,
        prefix='/users',
        tags=['Users'],
    )
    app.include_router(
        categories_router,
        prefix='/categories',
        tags=['Categories'],
    )
    app.include_router(
        locations_router,
        prefix='/locations',
        tags=['Locations'],
    )
    app.include_router(
        posts_router,
        prefix='/posts',
        tags=['Posts'],
    )
    app.include_router(
        comments_router,
        prefix='/comments',
        tags=['Comments'],
    )

    _fix_openapi_schema(app)

    return app


def _fix_openapi_schema(app: FastAPI) -> None:
    from fastapi.openapi.utils import get_openapi

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )

        def _fix_items(obj):
            if isinstance(obj, dict):
                if obj.get('type') == 'array':
                    items = obj.get('items', {})
                    if 'contentMediaType' in items:
                        items['format'] = 'binary'
                        del items['contentMediaType']
                for val in obj.values():
                    _fix_items(val)
            elif isinstance(obj, list):
                for item in obj:
                    _fix_items(item)

        _fix_items(schema)
        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi
