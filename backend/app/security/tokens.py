import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from ..config import JWT_ACCESS_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_REFRESH_EXPIRE_DAYS, JWT_SECRET_KEY


def create_access_token(practitioner_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    payload = {"sub": str(practitioner_id), "exp": expires_at}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return int(payload["sub"])


def generate_refresh_token() -> tuple[str, str, datetime]:
    raw_token = secrets.token_urlsafe(48)
    token_hash = hash_refresh_token(raw_token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    return raw_token, token_hash, expires_at


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
