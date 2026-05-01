from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.core.logging import setup_logging, get_logger
from src.api.users import user_router
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

    app.include_router(
        auth_router,
        prefix='/auth',
        tags=['Auth'],
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

    return app
