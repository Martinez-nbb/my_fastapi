from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base import (
    BaseCreatedAtSchema,
    BaseIdSchema,
    BasePublishedSchema,
)
from src.schemas.categories import CategoryResponseSchema
from src.schemas.locations import LocationResponseSchema
from src.schemas.users import UserResponseSchema


class PostBaseSchema(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description='Заголовок публикации (1-256 символов)',
        title='Заголовок',
    )
    text: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description='Текст публикации (содержимое статьи)',
        title='Текст публикации',
    )
    pub_date: datetime = Field(
        ...,
        description='Дата и время публикации',
        title='Дата публикации',
    )


class PostCreateSchema(PostBaseSchema, BasePublishedSchema):
    author_id: int = Field(
        ...,
        description='ID автора публикации (существующий пользователь)',
        examples=[1, 2, 42],
        title='ID автора',
    )
    location_id: int | None = Field(
        default=None,
        description='ID местоположения (опционально)',
        title='ID местоположения',
    )
    category_id: int | None = Field(
        default=None,
        description='ID категории (опционально)',
        title='ID категории',
    )


class PostUpdateSchema(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=256,
        description='Заголовок публикации',
    )
    text: str | None = Field(
        default=None,
        min_length=1,
        max_length=100000,
        description='Текст публикации',
    )
    pub_date: datetime | None = Field(
        default=None,
        description='Дата и время публикации',
    )
    is_published: bool | None = Field(
        default=None,
        description='Флаг публикации',
    )
    location_id: int | None = Field(
        default=None,
        description='ID местоположения',
    )
    category_id: int | None = Field(
        default=None,
        description='ID категории',
        ge=1,
    )


class PostResponseSchema(
    PostBaseSchema,
    BaseIdSchema,
    BaseCreatedAtSchema,
):
    is_published: bool = Field(
        default=True,
        description='Опубликовано (True = видно на сайте)',
        examples=[True, False],
    )
    author: UserResponseSchema = Field(
        ...,
        description='Автор публикации (объект пользователя)',
        title='Автор',
    )
    location: LocationResponseSchema | None = Field(
        default=None,
        description='Местоположение публикации (опционально)',
        title='Местоположение',
    )
    category: CategoryResponseSchema | None = Field(
        default=None,
        description='Категория публикации (опционально)',
        title='Категория',
    )
    image: str | None = Field(
        default=None,
        description='Путь к изображению публикации',
        title='Изображение',
    )
    model_config = ConfigDict(from_attributes=True, extra='ignore')
