import bcrypt
from rest.schema.token_schema import AuthResponseDTO, FullTokenDTO, RefreshTokenDTO
from rest.schema.user_schema import UserResponseDTO, UserLoginDTO, UserSignUpDTO
from rest.repository.token_repository import TokenRepository
from rest.repository.user_account_repository import UserAccountRepository
from rest.model.database import DB
from rest.util.token import verify_refresh_token, create_access_token
from rest.service.token_service import save_refresh_token
from rest.exceptions.exceptions import (UserAlreadyExistsException,
                                                UserNotFoundException,
                                                InvalidCredentialsException)

userAccountRepository = UserAccountRepository()
tokenRepository = TokenRepository()

def hashing_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

async def sign_up(userSignUpDTO: UserSignUpDTO, db: DB) -> AuthResponseDTO:
    if await userAccountRepository.get_user_by_email(userSignUpDTO.email, db):
        raise UserAlreadyExistsException()

    hashed_password = hashing_password(userSignUpDTO.password)

    saved_user = await userAccountRepository.save_user(UserSignUpDTO(
        username=userSignUpDTO.username,
        email=userSignUpDTO.email,
        password=hashed_password
    ), db)

    refresh_token = await save_refresh_token(userSignUpDTO.email, db)
    access_token = create_access_token(userSignUpDTO.email)

    return AuthResponseDTO (
        user=UserResponseDTO(
            id = saved_user.id,
            username = saved_user.username,
            email = saved_user.email,
        ),
        tokens=FullTokenDTO(
            refresh_token=refresh_token.refresh_token,
            access_token=access_token,
            token_type="Bearer"
        )
    )

async def log_in(userLoginDTO: UserLoginDTO, db: DB) -> AuthResponseDTO:
    db_user = await userAccountRepository.get_user_by_email(userLoginDTO.email, db)
    if not db_user:
        raise UserNotFoundException()

    if not verify_password(userLoginDTO.password, db_user.password):
        raise InvalidCredentialsException()

    refresh_token = await save_refresh_token(userLoginDTO.email, db)
    access_token = create_access_token(userLoginDTO.email)

    return AuthResponseDTO(
        user=UserResponseDTO(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
        ),
        tokens=FullTokenDTO(
            refresh_token=refresh_token.refresh_token,
            access_token=access_token,
            token_type="Bearer"
        )
    )

async def log_out(refreshTokenDTO: RefreshTokenDTO, db: DB) -> str:
    email = verify_refresh_token(refreshTokenDTO)
    user = await userAccountRepository.get_user_by_email(email, db)
    if not user:
        raise UserNotFoundException()
    user_id = user.id

    await tokenRepository.delete_refresh_token(user_id, db)
    return "Logged out successfully."

async def delete_account(refreshTokenDTO: RefreshTokenDTO, db: DB) -> str:
    email = verify_refresh_token(refreshTokenDTO)
    await userAccountRepository.delete_user_by_email(email, db)

    return "account deleted successfully"