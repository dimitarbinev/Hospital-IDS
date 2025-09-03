from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, ExpiredSignatureError
from jose.exceptions import JWTClaimsError, JWTError
from typing import Literal, Dict, Any

from rest.exceptions.exceptions import InvalidTokenException
from rest.schema.token_schema import RefreshTokenDTO
from rest.util.token import JWT_ALGORITHM, JWT_SECRET, JWT_AUDIENCE, JWT_ISSUER

bearer = HTTPBearer(auto_error=True)

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
        raise InvalidTokenException() from e
    except JWTClaimsError as e:
        raise InvalidTokenException() from e
    except JWTError as e:
        raise InvalidTokenException() from e


def verify_refresh_token(refreshTokenDTO: RefreshTokenDTO) -> int:
    payload = verify_token(refreshTokenDTO.refresh_token, expected_type="refresh")
    try:
        return int(payload["sub"])

    except InvalidTokenException:
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