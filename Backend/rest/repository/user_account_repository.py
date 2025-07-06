from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from rest.model.user_credentials_entity import User
from sqlalchemy.ext.asyncio import AsyncSession
from rest.exceptions.exceptions import (UserNotFoundException,
                                                DataBaseFailException)
from rest.schema.user_schema import UserSignUpDTO

class UserAccountRepository:

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession):
        try:
            result = await  db.execute(select(User).filter(User.email == email))
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            raise DataBaseFailException()

    @staticmethod
    async def save_user(userSignUpDTO: UserSignUpDTO, db: AsyncSession) -> User:
        user = User(
            username=userSignUpDTO.username,
            email=userSignUpDTO.email,
            password=userSignUpDTO.password
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete_user_by_email(email: str, db: AsyncSession):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFoundException()

        await db.delete(user)
        await db.commit()