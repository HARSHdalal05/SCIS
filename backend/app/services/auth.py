from datetime import datetime, timedelta, timezone

from jose import jwt

from ..config import settings


def create_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(hours=24)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
