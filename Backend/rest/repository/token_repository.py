from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from rest.exceptions.exceptions import NotExistingTokenException
from rest.model.token_entity import Token
from datetime import datetime

class TokenRepository:

    @staticmethod
    async def save_token(user_id: int, refresh_token: str, expires_at: datetime, created_at: datetime, db: AsyncSession):
        existing_token = await TokenRepository.get_refresh_token(user_id, db)
        if existing_token:
            await TokenRepository.delete_refresh_token(user_id, db)

        token = Token(
            user_id = user_id,
            refresh_token = refresh_token,
            expires_at = expires_at,
            created_at = created_at
        )

        db.add(token)
        await db.commit()
        await db.refresh(token)

    @staticmethod
    async def get_refresh_token(user_id: int, db: AsyncSession):
        result = await db.execute(select(Token).where(Token.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_refresh_token(user_id: int, db: AsyncSession):
        result = await db.execute(select(Token).where(Token.user_id == user_id))
        token = result.scalar_one_or_none()
        if not token:
            raise NotExistingTokenException()

        await db.delete(token)
        await db.commit()