from datetime import datetime
from typing import Type

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgres.models.refresh_token import RefreshToken as RefreshTokenModel


class RefreshTokenRepository:
    def __init__(self) -> None:
        self._model: Type[RefreshTokenModel] = RefreshTokenModel

    async def create(
        self,
        session: AsyncSession,
        token: str,
        user_id: int,
        expires_at: datetime,
    ) -> RefreshTokenModel:
        query = (
            insert(self._model)
            .values(
                token=token,
                user_id=user_id,
                expires_at=expires_at,
            )
            .returning(self._model)
        )
        return await session.scalar(query)

    async def get_by_token(self, session: AsyncSession, token: str) -> RefreshTokenModel | None:
        query = select(self._model).where(
            self._model.token == token,
            self._model.is_revoked == False,
        )
        return await session.scalar(query)

    async def revoke(self, session: AsyncSession, token: str) -> None:
        query = (
            update(self._model)
            .where(self._model.token == token)
            .values(is_revoked=True)
        )
        await session.execute(query)

    async def revoke_all_for_user(self, session: AsyncSession, user_id: int) -> None:
        query = (
            update(self._model)
            .where(
                self._model.user_id == user_id,
                self._model.is_revoked == False,
            )
            .values(is_revoked=True)
        )
        await session.execute(query)
