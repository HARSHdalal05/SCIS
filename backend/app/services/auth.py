from datetime import datetime, timedelta

from jose import jwt

from ..config import settings


def create_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
