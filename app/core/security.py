from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt,JWTError
from passlib.context import CryptContext

from app.core.config import settings

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES 
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def create_token(token_type: str, user_id: int, expires_delta: timedelta) -> str:
    """
    Generates a signed JWT with specified type and expiration.
    This function is reusable for both Access and Refresh tokens.
    """
    to_encode: dict[str, Any] = {"user_id": user_id, "type": token_type}
    
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode.update({"exp": expire, "sub": str(user_id)})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_access_token(user_id: int) -> str:
    return create_token(
        token_type=ACCESS_TOKEN_TYPE,
        user_id=user_id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(user_id: int) -> str:
    return create_token(
        token_type=REFRESH_TOKEN_TYPE,
        user_id=user_id,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Decodes and validates a JWT token.
    Returns the payload if valid, otherwise returns None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:

        return None