from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    jti: str | None = None


def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    iat = datetime.utcnow()
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": iat,
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str, verify_exp: bool = True) -> TokenPayload:
    """
    Decodifica um token JWT.

    Args:
        token: Token JWT a ser decodificado
        verify_exp: Se True, valida a expiração do token. Se False, permite tokens expirados.

    Returns:
        TokenPayload com os dados do token
    """
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_exp": verify_exp},
    )
    return TokenPayload(**payload)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
