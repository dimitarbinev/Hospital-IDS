from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose.exceptions import JWTClaimsError
from rest.exceptions.exceptions import InvalidTokenException
from rest.schema.token_schema import RefreshTokenDTO
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Literal
from uuid import uuid4
from jose import jwt, JWTError, ExpiredSignatureError
import os

JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-dev-key")
JWT_ALGORITHM = "HS256"
JWT_ISSUER = os.getenv("JWT_ISSUER", "hospital-ids")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "hospital-ids-api")

if JWT_SECRET == "fallback-secret-dev-key":
    raise RuntimeError("JWT_SECRET must be set")

ACCESS_EXPIRE_SECONDS = int(timedelta(minutes=15).total_seconds())
REFRESH_EXPIRE_SECONDS = int(timedelta(days=30).total_seconds())

bearer = HTTPBearer(auto_error=True)

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _ts(dt: datetime) -> int:
    return int(dt.timestamp())

def create_access_token(user_id: int) -> str:
    now = _now_utc()
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "access",
        "iat": _ts(now),
        "exp": _ts(now + timedelta(seconds=ACCESS_EXPIRE_SECONDS)),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM, headers={"typ": "JWT"})

def create_refresh_token(user_id: int) -> str:
    now = _now_utc()
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": _ts(now),
        "exp": _ts(now + timedelta(seconds=REFRESH_EXPIRE_SECONDS)),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM, headers={"typ": "JWT"})

def verify_token(token: str, expected_type: Literal["access", "refresh"]) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
        if payload.get("type") != expected_type:
            raise InvalidTokenException("wrong token type")
        sub = payload.get("sub")
        if not sub:
            raise InvalidTokenException("missing subject")
        return payload

    except ExpiredSignatureError as e:
        raise InvalidTokenException("token expired") from e
    except JWTClaimsError as e:
        raise InvalidTokenException("invalid claims") from e
    except JWTError as e:
        raise InvalidTokenException("invalid token") from e

def verify_refresh_token(refreshTokenDTO: RefreshTokenDTO) -> int:
    payload = verify_token(refreshTokenDTO.refresh_token, expected_type="refresh")
    try:
        return int(payload["sub"])

    except (TypeError, ValueError):
        raise InvalidTokenException("invalid subject in refresh token")

async def jwt_validation(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> int:
    token = creds.credentials
    try:
        hdr = jwt.get_unverified_header(token)

    except Exception:
        raise InvalidTokenException("Bad token header")

    if hdr.get("alg") != JWT_ALGORITHM:
        raise InvalidTokenException("Wrong algorithm")

    payload = verify_token(token=token, expected_type="access")
    sub = payload.get("sub")

    if not sub:
        raise InvalidTokenException("Missing subject")
    return int(sub)