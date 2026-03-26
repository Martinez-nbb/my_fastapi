from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator


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


class SlugValidatorMixin(BaseModel):
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, value: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise ValueError(
                'Slug должен содержать только латинские буквы, цифры, '
                'дефисы и подчеркивания'
            )
        return value


class EmailValidatorMixin(BaseModel):
    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return value
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError('Некорректный формат email адреса')
        return value


class UsernameValidatorMixin(BaseModel):
    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value) < 3 or len(value) > 150:
            raise ValueError(
                'Имя пользователя должно быть от 3 до 150 символов'
            )
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValueError(
                'Имя пользователя может содержать буквы, цифры и символы: '
                '@/./+/-/_'
            )
        return value


class TextValidatorMixin(BaseModel):
    @field_validator('text')
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value or len(value.strip()) == 0:
            raise ValueError('Текст не может быть пустым')
        return value.strip()
