from rest.exceptions.exceptions import NotExistingTokenException, DataBaseFailException
from rest.model.token_entity import Token

import hashlib
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

class TokenRepository:

    @staticmethod
    async def save_token(
        user_id: int,
        refresh_token: str,
        iat: int,
        exp: int,
        jti: str,
        db: AsyncSession,
    ):
        try:
            existing_token = await TokenRepository.get_refresh_token(user_id, db)
            if existing_token:
                await TokenRepository.delete_refresh_token(user_id, db)

            hashed_token = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()

            token = Token(
                user_id=user_id,
                refresh_token=hashed_token,
                iat=iat,
                exp=exp,
                jti=jti,
            )

            db.add(token)
            await db.commit()
            await db.refresh(token)

        except SQLAlchemyError:
            await db.rollback()
            raise DataBaseFailException()

    @staticmethod
    async def get_refresh_token(user_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Token).where(Token.user_id == user_id))
            return result.scalar_one_or_none()

        except SQLAlchemyError:
            await db.rollback()
            raise DataBaseFailException()

    @staticmethod
    async def delete_refresh_token(user_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Token).where(Token.user_id == user_id))
            token = result.scalar_one_or_none()
            if not token:
                raise NotExistingTokenException()

            await db.delete(token)
            await db.commit()

        except SQLAlchemyError:
            await db.rollback()
            raise DataBaseFailException()
