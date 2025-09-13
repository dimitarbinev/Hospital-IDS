from rest.service.user_account_service import sign_up, log_in, log_out, delete_account
from rest.model.database import DB
from rest.schema.token_schema import AuthResponseDTO, RefreshTokenDTO
from rest.schema.user_schema import UserSignUpDTO, UserLoginDTO

from fastapi import APIRouter, Body

user_router = APIRouter(prefix="/account")

@user_router.post("/signup", response_model=AuthResponseDTO)
async def sign_up_handler(userSignUpDTO: UserSignUpDTO, db: DB):
    return await sign_up(userSignUpDTO, db)

@user_router.post("/login", response_model=AuthResponseDTO)
async def log_in_handler(userLoginDTO: UserLoginDTO, db: DB):
    return await log_in(userLoginDTO, db)

@user_router.post("/logout")
async def log_out_handler(db: DB, refreshTokenDTO: RefreshTokenDTO = Body(...)):
    return await log_out(refreshTokenDTO, db)

@user_router.delete("/delete")
async def delete_account_handler(db: DB, refreshTokenDTO: RefreshTokenDTO = Body(...)):
    return await delete_account(refreshTokenDTO, db)