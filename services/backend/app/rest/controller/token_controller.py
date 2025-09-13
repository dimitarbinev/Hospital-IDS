from rest.model.database import DB
from rest.service.token_service import get_new_access_token
from rest.schema.token_schema import RefreshTokenDTO, AccessTokenDTO

from fastapi import APIRouter, Header

token_router = APIRouter(prefix="/auth")

token_router.post("/token", response_model=AccessTokenDTO)
async def get_new_token_handler(db: DB, refresh_token: str = Header(...)):
    refresh_dto = RefreshTokenDTO(refresh_token=refresh_token)
    return await get_new_access_token(refresh_dto, db)