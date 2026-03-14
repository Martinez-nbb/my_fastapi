from src.api.categories import router as categories_router
from src.api.comments import router as comments_router
from src.api.locations import router as locations_router
from src.api.posts import router as posts_router
from src.api.users import user_router

__all__ = [
    'categories_router',
    'comments_router',
    'locations_router',
    'posts_router',
    'user_router',
]
