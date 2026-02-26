from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from typing import Optional, List

from src.schemas.base import (
    BasePublishedSchema,   
    BaseCreatedAtSchema,   
    BaseIdSchema,       
)

from src.schemas.users import UserSchema
from src.schemas.locations import LocationResponseSchema
from src.schemas.categories import CategoryResponseSchema

class PostBaseSchema(BaseModel):
    
    title: str = Field(
        ..., 
        min_length=1,
        max_length=256,
        description="Заголовок публикации (1-256 символов)",
        title="Заголовок",
    )text: str = Field(
        ..., 
        min_length=1,
        max_length=100000,
        description="Текст публикации (содержимое статьи)",
        title="Текст публикации",
    )
    pub_date: datetime = Field(
        ..., 
        description="Дата и время публикации (для отложенных публикаций можно указать будущее время)",
        title="Дата публикации",
    )
class PostCreateSchema(PostBaseSchema, BasePublishedSchema):
    
    author_id: int = Field(
        ...,  
        description="ID автора публикации (существующий пользователь)",
        examples=[1, 2, 42],
        title="ID автора",
    )
    location_id: Optional[int] = Field(
        None,  
        description="ID местоположения (опционально)",
        title="ID местоположения",
    )
    
    category_id: Optional[int] = Field(
        None,  
        description="ID категории (опционально)",
        
        title="ID категории",
    )

class PostUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=256,
        description="Заголовок публикации",
    )
    text: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100000,
        description="Текст публикации",
    )
    pub_date: Optional[datetime] = Field(
        None,
        description="Дата и время публикации",
    )
    is_published: Optional[bool] = Field(
        None,
        description="Флаг публикации",
    )
    location_id: Optional[int] = Field(
        None,
        description="ID местоположения",
    )
    category_id: Optional[int] = Field(
        None,
        description="ID категории",
        ge=1,
    )


# =============================================================================
# СХЕМА 4: PostResponseSchema (Схема для ответа API)
# =============================================================================
class PostResponseSchema(PostBaseSchema, BaseIdSchema, BaseCreatedAtSchema):
    is_published: bool = Field(
        default=True,
        description="Опубликовано (True = видно на сайте)",
        examples=[True, False],
    )
    author: UserSchema = Field(
        ...,  
        
        description="Автор публикации (объект пользователя)",
        
        title="Автор",
    )
    location: Optional[LocationResponseSchema] = Field(
        None,
        description="Местоположение публикации (опционально)",
        title="Местоположение",
    )
    category: Optional[CategoryResponseSchema] = Field(
        None,
        description="Категория публикации (опционально)",
        title="Категория",
    )
    image: Optional[str] = Field(
        None,
        description="Путь к изображению публикации",
        examples=[
            "/media/post_images/moscow.jpg",
            "/media/post_images/recipe.png",
            None, 
        ],
        
        title="Изображение",
    )
    model_config = ConfigDict(from_attributes=True)