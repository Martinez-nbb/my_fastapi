from pydantic import BaseModel, Field, SecretStr, EmailStr

from typing import Optional
class UserSchema(BaseModel):
    
    username: str = Field(
        min_length=3,
        max_length=150,
        description="Имя пользователя (уникальное, 3-150 символов)",
        title="Имя пользователя",
    )
    password: SecretStr = Field(
        min_length=8,
        description="Пароль пользователя (минимум 8 символов)",
        title="Пароль",
    )
    email: Optional[str] = Field(
        None,
        description="Email адрес пользователя",
        title="Email",
    )
    class Config:
        # from_attributes=True позволяет создавать схему из ORM-объектов
        from_attributes = True
class UserCreateSchema(BaseModel):
    
    # Поле username со строгой валидацией
    username: str = Field(
        ...,  # Обязательное поле
        min_length=3,
        max_length=150,
        pattern=r'^[\w.@+-]+$',
        description="Имя пользователя (только буквы, цифры и @/+/-/_)",
        title="Имя пользователя",
    )
    password: str = Field(
        ..., 
        min_length=8,
        description="Пароль (минимум 8 символов)",
        examples=["********"],
        title="Пароль",
    )
    
    # Поле email с автоматической валидацией
    email: EmailStr = Field(
        ...,
        description="Email адрес",
        title="Email",
    )
class UserResponseSchema(BaseModel):
    
    # Поле id (первичный ключ)
    id: int = Field(
        ..., 
        description="Уникальный идентификатор пользователя",
        ge=1,
        title="ID",
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="Имя пользователя",
        title="Имя пользователя",
    )
    
    email: str = Field(
        ...,  
        description="Email адрес",
        title="Email",
    )
    is_active: bool = Field(
        default=True, 
        description="Активен ли пользователь",
        title="Статус активности",
    )
    class Config:
        # from_attributes=True для работы с ORM объектами
        from_attributes = True