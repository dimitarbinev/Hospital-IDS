from rest.exceptions.exceptions import InvalidTokenException
from rest.schema.token_schema import RefreshTokenDTO
from rest.util.token import JWT_ALGORITHM, JWT_SECRET, JWT_AUDIENCE, JWT_ISSUER, JWT_LEEWAY

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, ExpiredSignatureError
from jose.exceptions import JWTClaimsError, JWTError
from typing import Literal, Dict, Any
from uuid import UUID
from datetime import datetime, timezone

bearer = HTTPBearer(auto_error=True)

def _uuid_v4_ok(value: str | None) -> bool:
    if not value:
        return False
    try:
        UUID(value, version=4)
        return True
    except Exception:
        return False

def verify_token(token: str, expected_type: Literal["access", "refresh"]) -> Dict[str, Any]:
    # header validation
    try:
        hdr = jwt.get_unverified_header(token)
    except Exception:
        raise InvalidTokenException("Bad token header")
    if hdr.get("alg") != JWT_ALGORITHM:
        raise InvalidTokenException("Wrong algorithm")
    if hdr.get("typ") and hdr["typ"] != "JWT":
        raise InvalidTokenException("Wrong header typ")

    # payload validation
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
            options={
                "require_exp": True,
                "require_iat": True,
                "require_aud": True,
                "require_sub": True,
                "verify_jti": True,
                "verify_exp": True,
                "verify_iat": True,
                "leeway": JWT_LEEWAY,
            },
        )
    except ExpiredSignatureError as e:
        raise InvalidTokenException("token expired") from e
    except (JWTClaimsError, JWTError) as e:
        raise InvalidTokenException("invalid token") from e

    # type validation
    if payload.get("type") != expected_type:
        raise InvalidTokenException("wrong token type")

    # subject validation
    sub = payload.get("sub")
    if sub is None:
        raise InvalidTokenException("missing subject")

    # issued at validation
    iat = payload.get("iat")
    if not isinstance(iat, (int, float)):
        raise InvalidTokenException("invalid iat")
    now_ts = datetime.now(timezone.utc).timestamp()
    if (iat - now_ts) > JWT_LEEWAY:
        raise InvalidTokenException("iat in the future")

    # uuid validation
    jti = payload.get("jti")
    if jti is not None and not _uuid_v4_ok(jti):
        raise InvalidTokenException("bad jti")

    return payload


def verify_refresh_token(refreshTokenDTO: RefreshTokenDTO) -> int:
    payload = verify_token(refreshTokenDTO.refresh_token, expected_type="refresh")
    try:
        return int(payload["sub"])

    except (ValueError, TypeError):
        raise InvalidTokenException("invalid subject in refresh token")

async def access_token_validation(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> int:
    payload = verify_token(creds.credentials, expected_type="access")
    try:
        return int(payload["sub"])
    except Exception:
        raise InvalidTokenException("invalid subject format")