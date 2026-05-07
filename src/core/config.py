from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORIGINS: str = '*'
    PORT: int = 8000
    ROOT_PATH: str = '/api/v1'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_AUTH_KEY: SecretStr = SecretStr('your-secret-key-change-in-production')
    AUTH_ALGORITHM: str = 'HS256'

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str = 'myfastapi'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: SecretStr = SecretStr('postgres')
    POSTGRES_PASSWORD: SecretStr = SecretStr('postgres')

    @property
    def database_url(self) -> str:
        creds = f'{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}'
        return f'postgresql+psycopg2://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
