from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base import (
    BaseCreatedAtSchema,
    BaseIdSchema,
    BasePublishedSchema,
)
from src.schemas.users import UserResponseSchema


class CommentBaseSchema(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description='Текст комментария (1-1000 символов)',
        title='Текст комментария',
    )


class CommentCreateSchema(CommentBaseSchema, BasePublishedSchema):
    post_id: int = Field(
        ...,
        description='ID публикации, к которой относится комментарий',
        title='ID публикации',
    )


class CommentUpdateSchema(BaseModel):
    text: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
        description='Текст комментария',
    )
    is_published: bool | None = Field(
        default=None,
        description='Флаг публикации',
    )


class CommentResponseSchema(
    CommentBaseSchema,
    BaseIdSchema,
    BaseCreatedAtSchema,
):
    is_published: bool = Field(
        default=True,
        description='Опубликовано',
    )
    author: UserResponseSchema = Field(
        ...,
        description='Автор комментария',
        title='Автор',
    )
    post_id: int = Field(
        ...,
        description='ID публикации, к которой относится комментарий',
        title='ID публикации',
    )
    model_config = ConfigDict(from_attributes=True, extra='ignore')
