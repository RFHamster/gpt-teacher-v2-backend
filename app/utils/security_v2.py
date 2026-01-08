from datetime import datetime, timedelta, timezone
import hashlib

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


def _normalize_password(password: str) -> bytes:
    """
    Normaliza a senha para contornar a limitação de 72 bytes do bcrypt.
    Faz hash SHA256 da senha antes de passar para o bcrypt.
    """
    return hashlib.sha256(password.encode()).hexdigest().encode()


def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    iat = datetime.now(timezone.utc)
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
    normalized = _normalize_password(plain_password)
    return pwd_context.verify(normalized, hashed_password)


def get_password_hash(password: str) -> str:
    normalized = _normalize_password(password)
    return pwd_context.hash(normalized)
