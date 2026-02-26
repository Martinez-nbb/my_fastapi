from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from src.schemas.base import (
    BasePublishedSchema,   
    BaseCreatedAtSchema,   
    BaseIdSchema,      
)

class CategoryBaseSchema(BaseModel):
    title: str = Field(
        ..., 
        
        min_length=1,
        max_length=256,
        description="Заголовок категории (1-256 символов)",
        title="Заголовок",
    )
    description: str = Field(
        ..., 
        min_length=1,
        max_length=10000,
        description="Подробное описание категории",
        title="Описание",
    )
    slug: str = Field(
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        
       description="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание",
        title="Slug (URL-идентификатор)",
    )
class CategoryCreateSchema(CategoryBaseSchema, BasePublishedSchema):
    pass
class CategoryUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        None,
        
        min_length=1,
        max_length=256,
        
        description="Заголовок категории",
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=10000,
        description="Описание категории",
    )
    slug: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Slug (URL-идентификатор)",
    )
    is_published: Optional[bool] = Field(
        None,
        description="Флаг публикации (True = опубликовано, False = черновик)",
        examples=[True, False],
    )

class CategoryResponseSchema(CategoryBaseSchema, BaseIdSchema, BaseCreatedAtSchema):
    is_published: bool = Field(
        default=True,
        description="Опубликовано (True = видно на сайте, False = черновик)",
        examples=[True, False],
        title="Статус публикации",
    )
    # model_config — новый способ настройки в Pydantic v2
    # Заменяет внутренний класс Config из Pydantic v1
    model_config = ConfigDict(
        # from_attributes=True позволяет создавать схему из ORM объектов
        from_attributes=True,
    )