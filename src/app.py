
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from src.api.categories import router as categories_router

from src.api.locations import router as locations_router

from src.api.posts import router as posts_router

from src.api.comments import router as comments_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="my_fastapi API",
        
        description="""
## Блог-платформа на FastAPI

REST API для блога
        """,
        
        version="1.0.0",
        
        # root_path — базовый путь для всех endpoints
        # Все роуты будут иметь префикс /api/v1
        root_path="/api/v1",
    )
    app.add_middleware(
        CORSMiddleware,
        
        allow_origins=["*"],
        
        allow_credentials=True,
        
        allow_methods=["*"],
        
        allow_headers=["*"],
    )
    
    app.include_router(
        categories_router,
        prefix="/categories",
        tags=["Categories"],  # Группа в Swagger UI
    )
    
    app.include_router(
        locations_router,
        prefix="/locations",
        tags=["Locations"],
    )
    
    app.include_router(
        posts_router,
        prefix="/posts",
        tags=["Posts"],
    )
    
    app.include_router(
        comments_router,
        prefix="/comments",
        tags=["Comments"],
    )
    
    @app.get(
        "/health",
        tags=["Health"], 
        summary="Health check",
        description="Проверка работоспособности API. Возвращает статус сервиса.",
    )
    async def health_check():
        
        return {
            "status": "ok",
            "service": "my_fastapi",
            "version": "1.0.0",
        }
    return app