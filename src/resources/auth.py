import asyncio
import logging

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', auto_error=False
)

BCRYPT_MAX_BYTES = 72


def _truncate_password(password: str) -> str:
    password_bytes = password.encode('utf-8')[:BCRYPT_MAX_BYTES]
    if len(password.encode('utf-8')) > BCRYPT_MAX_BYTES:
        logger.warning("Пароль превышает 72 байта в UTF-8 и будет обрезан")
    return password_bytes.decode('utf-8', errors='ignore')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_truncate_password(plain_password), hashed_password)


async def async_verify_password(plain_password: str, hashed_password: str) -> bool:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, verify_password, plain_password, hashed_password
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(_truncate_password(password))


async def async_get_password_hash(password: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_password_hash, password)
