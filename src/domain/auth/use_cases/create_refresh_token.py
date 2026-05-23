import secrets
from datetime import datetime, timedelta, timezone

from src.core.config import settings
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.refresh_token import RefreshTokenRepository
from src.core.logging import get_logger

logger = get_logger(__name__)


class CreateRefreshTokenUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = RefreshTokenRepository()

    async def execute(self, user_id: int) -> str:
        token = secrets.token_urlsafe(48)
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )

        async with self._database.session() as session:
            await self._repo.create(
                session=session,
                token=token,
                user_id=user_id,
                expires_at=expires_at,
            )

        logger.info(f"Refresh token created for user_id={user_id}")
        return token
