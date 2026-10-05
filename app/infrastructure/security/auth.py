from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.infrastructure.security.jwt import decode_access_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[!] Token inválido!")

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[!] Token inválido ou expirado.")

    repository = UserRepository(db)
    user = repository.get_by_id(int(user_id))

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[!] Usuário não encontrado.")

    return user