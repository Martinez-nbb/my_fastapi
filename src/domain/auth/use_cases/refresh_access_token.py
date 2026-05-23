from datetime import datetime, timezone

from src.core.config import settings
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.refresh_token import RefreshTokenRepository
from src.infrastructure.postgres.repositories.user import UserRepository
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.domain.auth.use_cases.create_refresh_token import CreateRefreshTokenUseCase
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import InvalidCredentialsException
from src.core.logging import get_logger

logger = get_logger(__name__)


class RefreshAccessTokenUseCase:
    def __init__(self) -> None:
        self._database = database
        self._refresh_repo = RefreshTokenRepository()
        self._user_repo = UserRepository()
        self._access_token_uc = CreateAccessTokenUseCase()
        self._refresh_token_uc = CreateRefreshTokenUseCase()

    async def execute(self, refresh_token: str) -> tuple[str, str]:
        async with self._database.session() as session:
            stored = await self._refresh_repo.get_by_token(
                session=session, token=refresh_token,
            )
            if not stored:
                logger.warning("Invalid or revoked refresh token")
                raise InvalidCredentialsException()

            if stored.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                logger.warning("Expired refresh token")
                await self._refresh_repo.revoke(session=session, token=refresh_token)
                raise InvalidCredentialsException()

            try:
                user = await self._user_repo.get(session=session, user_id=stored.user_id)
            except UserNotFoundException:
                logger.error(f"User not found for refresh token: user_id={stored.user_id}")
                raise InvalidCredentialsException()

            await self._refresh_repo.revoke(session=session, token=refresh_token)

        new_access_token = await self._access_token_uc.execute(username=user.username)
        new_refresh_token = await self._refresh_token_uc.execute(user_id=user.id)

        logger.info(f"Tokens refreshed for user_id={user.id}")
        return new_access_token, new_refresh_token
