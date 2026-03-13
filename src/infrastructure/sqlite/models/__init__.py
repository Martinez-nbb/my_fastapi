# Импортируем модели для регистрации в Base.metadata
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.models.comment import Comment

__all__ = ['User', 'Category', 'Location', 'Post', 'Comment']
