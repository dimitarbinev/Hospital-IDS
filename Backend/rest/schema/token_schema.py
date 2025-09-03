from rest.schema.user_schema import UserResponseDTO

from pydantic import BaseModel

class RefreshTokenDTO(BaseModel):
    refresh_token: str
    token_type: str = "Bearer"

class AccessTokenDTO(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class FullTokenDTO(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str = "Bearer"

class AuthResponseDTO(BaseModel):
    user: UserResponseDTO
    tokens: FullTokenDTO