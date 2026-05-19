from typing import Dict, Any

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import UnauthorizedError


security = HTTPBearer(scheme_name="bearerAuth")


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        return payload

    except JWTError:
        raise UnauthorizedError(
            "invalid_or_expired_token",
            code="INVALID_TOKEN",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
):
    token = credentials.credentials

    payload = decode_token(token)

    subject = payload.get("sub")

    if not subject:
        raise UnauthorizedError(
            "invalid_token_subject",
            code="INVALID_SUBJECT",
        )

    return int(subject)
