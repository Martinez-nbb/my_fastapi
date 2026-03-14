from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base import (
    BaseCreatedAtSchema,
    BaseIdSchema,
    BasePublishedSchema,
)


class LocationBaseSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description='Название места (город, регион, страна)',
        title='Название места',
    )


class LocationCreateSchema(LocationBaseSchema, BasePublishedSchema):
    pass


class LocationUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=256,
        description='Название места',
    )
    is_published: bool | None = Field(
        default=None,
        description='Флаг публикации',
        examples=[True, False],
    )


class LocationResponseSchema(
    LocationBaseSchema,
    BaseIdSchema,
    BaseCreatedAtSchema,
):
    is_published: bool = Field(
        default=True,
        description='Опубликовано',
    )
    model_config = ConfigDict(from_attributes=True)
