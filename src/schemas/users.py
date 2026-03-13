from pydantic import BaseModel, Field, SecretStr, EmailStr

from typing import Optional
from datetime import datetime

from src.schemas.base import BaseIdSchema, BaseCreatedAtSchema

class UserBaseSchema(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=150,
        description="Имя пользователя (уникальное, 3-150 символов)",
        title="Имя пользователя",
    )
    email: Optional[str] = Field(
        None,
        description="Email адрес пользователя",
        title="Email",
    )
    first_name: str = Field(
        default='',
        description="Имя пользователя",
        title="Имя",
    )
    last_name: str = Field(
        default='',
        description="Фамилия пользователя",
        title="Фамилия",
    )


class UserCreateSchema(UserBaseSchema):
    password: str = Field(
        ...,
        min_length=8,
        description="Пароль (минимум 8 символов)",
        examples=["********"],
        title="Пароль",
    )


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=150,
        description="Имя пользователя",
    )
    email: Optional[str] = Field(
        None,
        description="Email адрес",
    )
    first_name: Optional[str] = Field(
        None,
        description="Имя",
    )
    last_name: Optional[str] = Field(
        None,
        description="Фамилия",
    )
    is_active: Optional[bool] = Field(
        None,
        description="Активен ли пользователь",
    )


class UserResponseSchema(UserBaseSchema, BaseIdSchema):
    is_active: bool = Field(
        default=True,
        description="Активен ли пользователь",
        title="Статус активности",
    )
    is_superuser: bool = Field(
        default=False,
        description="Является ли суперпользователем",
        title="Суперпользователь",
    )
    is_staff: bool = Field(
        default=False,
        description="Является ли сотрудником",
        title="Сотрудник",
    )
    date_joined: datetime = Field(
        default=None,
        description="Дата регистрации",
        title="Дата регистрации",
    )

    class Config:
        from_attributes = True
