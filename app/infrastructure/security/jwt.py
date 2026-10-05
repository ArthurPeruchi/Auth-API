from datetime import datetime, timedelta, timezone
from decouple import config
import jwt

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = config("JWT_EXPIRE_MINUTES", cast=int)

def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    
    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])