from pydantic import BaseModel, Field, ConfigDict

from typing import Optional

from src.schemas.base import (
    BasePublishedSchema,    
    BaseCreatedAtSchema,    
    BaseIdSchema,          
)
class LocationBaseSchema(BaseModel):
    
    name: str = Field(
        ..., 
        min_length=1,
        max_length=256,
        description="Название места (город, регион, страна)",
        title="Название места",
    )


class LocationCreateSchema(LocationBaseSchema, BasePublishedSchema):
    pass


class LocationUpdateSchema(BaseModel):
    name: Optional[str] = Field(
        None,  # default=None — не обязательное
        min_length=1,
        max_length=256,
        description="Название места",
    )
    is_published: Optional[bool] = Field(
        None,
        description="Флаг публикации",
        examples=[True, False],
    )


class LocationResponseSchema(LocationBaseSchema, BaseIdSchema, BaseCreatedAtSchema):
    is_published: bool = Field(
        default=True,
        description="Опубликовано",
    )
    model_config = ConfigDict(from_attributes=True)