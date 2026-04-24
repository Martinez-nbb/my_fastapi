from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(description="Token type (bearer)")


class TokenData(BaseModel):
    username: str | None = None


class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1)


class UserRegister(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1)
    email: str = Field(default='')
    first_name: str = Field(default='')
    last_name: str = Field(default='')
