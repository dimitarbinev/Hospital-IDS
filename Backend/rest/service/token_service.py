from rest.model.database import DB
from rest.repository.token_repository import TokenRepository
from rest.repository.user_account_repository import UserAccountRepository
from rest.schema.token_schema import RefreshTokenDTO, AccessTokenDTO
from rest.exceptions.exceptions import (
                                                InvalidTokenException,
                                                UserNotFoundException,
                                                NotExistingTokenException
                                                )
from rest.util.token import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from datetime import datetime, timedelta

REFRESH_EXPIRE_SECONDS = 30 * 24 * 60 * 60

userAccountRepository = UserAccountRepository()
tokenRepository = TokenRepository()

async def save_refresh_token(email: str, db: DB) -> RefreshTokenDTO:
    user = await userAccountRepository.get_user_by_email(email, db)
    if not user:
        raise UserNotFoundException()

    refresh_token = create_refresh_token(email)

    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(seconds=REFRESH_EXPIRE_SECONDS)

    await tokenRepository.save_token(user.id, refresh_token, expires_at, created_at, db)

    return RefreshTokenDTO(
        refresh_token=refresh_token,
        token_type="Bearer"
    )

async def get_refresh_token(refreshTokenDTO: RefreshTokenDTO, db: DB) -> RefreshTokenDTO:
    email = verify_refresh_token(refreshTokenDTO)
    user = await userAccountRepository.get_user_by_email(email, db)
    if not user:
        raise UserNotFoundException()
    user_id = user.id

    token = await tokenRepository.get_refresh_token(user_id, db)
    if not token or token.refresh_token != refreshTokenDTO.refresh_token or token.expires_at < datetime.utcnow():
        raise InvalidTokenException()

    return RefreshTokenDTO(
        refresh_token=refreshTokenDTO.refresh_token,
        token_type="Bearer"
    )

async def get_new_access_token(refreshTokenDTO: RefreshTokenDTO, db: DB) -> AccessTokenDTO:
    email = verify_refresh_token(refreshTokenDTO)
    user = await userAccountRepository.get_user_by_email(email, db)
    if not user:
        raise UserNotFoundException()
    user_id = user.id

    stored_refresh_token = await tokenRepository.get_refresh_token(user_id, db)
    if not stored_refresh_token:
        raise NotExistingTokenException()
    if stored_refresh_token.refresh_token != refreshTokenDTO.refresh_token or stored_refresh_token.expires_at < datetime.utcnow():
        raise InvalidTokenException()

    access_token = create_access_token(email)
    return AccessTokenDTO (
        access_token=access_token,
        token_type="Bearer"
    )

async def delete_refresh_token(refreshTokenDTO: RefreshTokenDTO, db: DB) -> str:
    email = verify_refresh_token(refreshTokenDTO)
    user = await userAccountRepository.get_user_by_email(email, db)
    if not user:
        raise UserNotFoundException()
    user_id = user.id

    await tokenRepository.delete_refresh_token(user_id, db)
    return "token deleted successfully"