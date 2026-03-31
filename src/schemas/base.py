from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator, model_validator
from fastapi import HTTPException, status


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


def validate_slug(value: str) -> str:
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Slug должен содержать только латинские буквы, цифры, дефисы и подчеркивания'
        )
    return value


def validate_email(value: str | None) -> str | None:
    if value is None:
        return value
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Некорректный формат email адреса'
        )
    return value


def validate_username(value: str) -> str:
    if len(value) < 3 or len(value) > 150:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Имя пользователя должно быть от 3 до 150 символов'
        )
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Имя пользователя может содержать буквы, цифры и символы: @/./+/-/_'
        )
    return value


def validate_text(value: str) -> str:
    if not value or len(value.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Текст не может быть пустым'
        )
    return value.strip()
