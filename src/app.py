from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.users import user_router
from src.api.categories import router as categories_router
from src.api.locations import router as locations_router
from src.api.posts import router as posts_router
from src.api.comments import router as comments_router
from src.api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path='/api/v1')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

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
