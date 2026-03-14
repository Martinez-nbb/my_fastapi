from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    username: str = Field(
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
    first_name: str = Field(
        default='',
        description='Имя пользователя',
        title='Имя',
    )
    last_name: str = Field(
        default='',
        description='Фамилия пользователя',
        title='Фамилия',
    )


class UserCreateSchema(UserBaseSchema):
    password: str = Field(
        ...,
        min_length=8,
        description='Пароль (минимум 8 символов)',
        examples=['********'],
        title='Пароль',
    )


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
        description='Имя',
    )
    last_name: str | None = Field(
        default=None,
        description='Фамилия',
    )
    is_active: bool | None = Field(
        default=None,
        description='Активен ли пользователь',
    )


class UserResponseSchema(UserBaseSchema):
    id: int = Field(
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

    model_config = {'from_attributes': True}
