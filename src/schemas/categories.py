from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base import BaseCreatedAtSchema, BaseIdSchema, BasePublishedSchema


class CategoryBaseSchema(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description='Заголовок категории (1-256 символов)',
        title='Заголовок',
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description='Подробное описание категории',
        title='Описание',
    )
    slug: str = Field(
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор страницы для URL',
        title='Slug (URL-идентификатор)',
    )


class CategoryCreateSchema(CategoryBaseSchema, BasePublishedSchema):
    pass


class CategoryUpdateSchema(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=256,
        description='Заголовок категории',
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=10000,
        description='Описание категории',
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Slug (URL-идентификатор)',
    )
    is_published: bool | None = Field(
        default=None,
        description='Флаг публикации',
        examples=[True, False],
    )


class CategoryResponseSchema(CategoryBaseSchema, BaseIdSchema, BaseCreatedAtSchema):
    is_published: bool = Field(
        default=True,
        description='Опубликовано',
        examples=[True, False],
        title='Статус публикации',
    )
    model_config = ConfigDict(from_attributes=True)
