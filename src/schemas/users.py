from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

from src.schemas.base import (
    BaseIdSchema,
    validate_email,
    validate_username,
)


class UserBaseSchema(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description='Имя пользователя (уникальное, 3-150 символов)',
        title='Имя пользователя',
    )
    email: str | None = Field(
        default=None,
        description='Email адрес пользователя',
        title='Email',
    )
    first_name: str | None = Field(
        default=None,
        max_length=150,
        description='Имя пользователя',
        title='Имя',
    )
    last_name: str | None = Field(
        default=None,
        max_length=150,
        description='Фамилия пользователя',
        title='Фамилия',
    )

    @field_validator('username')
    @classmethod
    def validate_username_field(cls, value: str) -> str:
        return validate_username(value)

    @field_validator('email')
    @classmethod
    def validate_email_field(cls, value: str | None) -> str | None:
        return validate_email(value)


class UserCreateSchema(UserBaseSchema):
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=72,
        description='Пароль (минимум 8 символов, максимум 72)',
        examples=['********'],
        title='Пароль',
    )

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, value: SecretStr) -> SecretStr:
        password_str = value.get_secret_value()
        # Проверяем длину в байтах (bcrypt ограничение)
        if len(password_str.encode('utf-8')) > 72:
            raise ValueError('Пароль не может быть длиннее 72 байт')
        return value


class UserUpdateSchema(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
        description='Имя пользователя',
    )
    email: str | None = Field(
        default=None,
        description='Email адрес',
    )
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
        description='Имя',
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
        description='Фамилия',
    )
    is_active: bool | None = Field(
        default=None,
        description='Активен ли пользователь',
    )

    @field_validator('username')
    @classmethod
    def validate_username_field(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_username(value)

    @field_validator('email')
    @classmethod
    def validate_email_field(cls, value: str | None) -> str | None:
        return validate_email(value)


class UserResponseSchema(UserBaseSchema, BaseIdSchema):
    id: int = Field(
        ...,
        description='Уникальный идентификатор пользователя',
        ge=1,
        title='ID',
    )
    is_active: bool = Field(
        default=True,
        description='Активен ли пользователь',
        title='Статус активности',
    )
    is_superuser: bool = Field(
        default=False,
        description='Является ли суперпользователем',
        title='Суперпользователь',
    )
    is_staff: bool = Field(
        default=False,
        description='Является ли сотрудником',
        title='Сотрудник',
    )

    model_config = ConfigDict(from_attributes=True)
