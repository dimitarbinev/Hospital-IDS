from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from uuid import uuid4
from jose import jwt
import os

from rest.exceptions.exceptions import InvalidTokenException
from rest.schema.token_schema import RefreshTokenDTO

JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-dev-key")
JWT_ALGORITHM = "HS256"
JWT_ISSUER = os.getenv("JWT_ISSUER", "hospital-ids")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "hospital-ids-api")
JWT_LEEWAY = 30

if JWT_SECRET == "fallback-secret-dev-key":
    raise RuntimeError("JWT_SECRET must be set")

ACCESS_EXPIRE_SECONDS = int(timedelta(minutes=15).total_seconds())
REFRESH_EXPIRE_SECONDS = int(timedelta(days=30).total_seconds())

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
        "leeway": JWT_LEEWAY,
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
        "leeway": JWT_LEEWAY,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM, headers={"typ": "JWT"})