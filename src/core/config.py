from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORIGINS: str = '*'
    PORT: int = 8000
    ROOT_PATH: str = '/api/v1'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr = SecretStr('your-secret-key-change-in-production')
    AUTH_ALGORITHM: str = 'HS256'

    SQLITE_URL: str = 'sqlite:///db.sqlite3'


settings = Settings()
