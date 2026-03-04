from __future__ import annotations

import time
import uuid

from jose import JWTError, jwt  # noqa: F401  (JWTError re-exported for deps)
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------------------
# Password
# ---------------------------------------------------------------------------

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------

def create_access_token(user_id: int, role: str) -> tuple[str, str, int]:
    """Returns (token, jti, exp_unix_timestamp)."""
    now = int(time.time())
    exp = now + settings.access_token_expire_minutes * 60
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(user_id),
        "role": role,
        "jti": jti,
        "iat": now,
        "exp": exp,
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return token, jti, exp


def decode_token(token: str) -> dict:
    """Raises jose.JWTError on invalid / expired token."""
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


def remaining_ttl(exp: int) -> int:
    """Seconds remaining until token expiry (minimum 0)."""
    return max(0, exp - int(time.time()))