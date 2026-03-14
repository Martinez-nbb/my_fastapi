from datetime import datetime

from pydantic import BaseModel, Field


class BasePublishedSchema(BaseModel):
    is_published: bool = Field(
        default=True,
        description='Опубликовано',
        title='Флаг публикации',
    )


class BaseCreatedAtSchema(BaseModel):
    created_at: datetime | None = Field(
        default=None,
        description='Дата и время создания записи',
        title='Дата создания',
    )


class BaseIdSchema(BaseModel):
    id: int = Field(
        description='Уникальный идентификатор записи (первичный ключ)',
        title='ID',
    )


class BaseTimestampSchema(BaseModel):
    created_at: datetime = Field(
        description='Дата и время создания записи',
        examples=['2024-01-15T10:30:00'],
    )
    updated_at: datetime | None = Field(
        default=None,
        description='Дата и время последнего обновления',
    )
