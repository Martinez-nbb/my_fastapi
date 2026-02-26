from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime

from typing import Optional

from src.schemas.base import (
    BasePublishedSchema,   
    BaseCreatedAtSchema,   
    BaseIdSchema,       
)
from src.schemas.users import UserSchema

class CommentBaseSchema(BaseModel):
    text: str = Field(
        ..., 
        min_length=1,
        max_length=1000,
        description="Текст комментария (1-1000 символов)",
        title="Текст комментария",
    )

class CommentCreateSchema(CommentBaseSchema, BasePublishedSchema):
    post_id: int = Field(
        ...,
        description="ID публикации, к которой относится комментарий",
        title="ID публикации",
    )
    author_id: int = Field(
        ..., 
        description="ID автора комментария",
        title="ID автора",
    )

class CommentUpdateSchema(BaseModel):
    text: Optional[str] = Field(
        None,
        min_length=1,
        max_length=1000,
        description="Текст комментария",
    )
    is_published: Optional[bool] = Field(
        None,
        description="Флаг публикации",
    )

class CommentResponseSchema(CommentBaseSchema, BaseIdSchema, BaseCreatedAtSchema):
    is_published: bool = Field(
        default=True,
        description="Опубликовано",
    )
    author: UserSchema = Field(
        ...,
        description="Автор комментария",
        title="Автор",
    )
    
    post_id: int = Field(
        ...,
        description="ID публикации, к которой относится комментарий",
        title="ID публикации",
    )
    model_config = ConfigDict(from_attributes=True)