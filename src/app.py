from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
def create_app() -> FastAPI:
    
    app = FastAPI(
        title="my_fastapi API",
        
        description="""
## Блог-платформа на FastAPI

REST API для блога с полным CRUD для следующих сущностей:

- **Категории** — рубрики публикаций
- **Местоположения** — географические метки  
- **Публикации** — статьи блога
- **Комментарии** — комментарии к публикациям
        """,
        
        # root_path — базовый путь для всех endpoints
        root_path="/api/v1",
    )
    
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(base_router, prefix="/base", tags=["Base APIs"])
    return app