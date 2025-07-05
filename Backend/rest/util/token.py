from Backend.rest.exceptions.exceptions import InvalidTokenException
from Backend.rest.schema.token_schema import RefreshTokenDTO
from datetime import datetime, timedelta
from typing import Dict, Any
from jose import jwt, JWTError
import os

JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-dev-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_SECONDS = int(timedelta(minutes=15).total_seconds())
REFRESH_EXPIRE_SECONDS = int(timedelta(days=30).total_seconds())

def create_token(email: str, expires_delta: int, token_type: str = "access") -> str:
    to_encode = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(seconds=expires_delta),
        "type": token_type,
        "iat": datetime.utcnow()
    }
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(email: str, expire_delta: int = REFRESH_EXPIRE_SECONDS) -> str:
    return create_token(email, expire_delta, "refresh")

def create_access_token(email: str, expires_delta: int = JWT_EXPIRE_SECONDS) -> str:
    return create_token(email, expires_delta, "access")

def verify_token(token: str, expected_type: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if payload.get("type") != expected_type:
            raise InvalidTokenException()

        if not payload.get("sub"):
            raise InvalidTokenException()

        return payload
    except JWTError:
        raise InvalidTokenException()

def verify_refresh_token(refreshTokenDTO: RefreshTokenDTO) -> str:
    payload = verify_token(refreshTokenDTO.refresh_token, "refresh")
    return payload["sub"]