from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.repositories.user_repository import UserRepository
from app.usecases.auth_usecase import AuthUseCase, InvalidCredentialsError
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from app.infrastructure.security.auth import get_current_user
from app.schemas.user_schema import UserResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_usecase(db: Session = Depends(get_db)) -> AuthUseCase:
    repository = UserRepository(db)
    password_hasher = Argon2PasswordHasher()

    return AuthUseCase(repository, password_hasher)

@router.post("", response_model=TokenResponse, status_code=status.HTTP_200_OK)

def login(data: LoginRequest, usecase: AuthUseCase = Depends(get_auth_usecase)):
    try:
        return usecase.login(data)

    except InvalidCredentialsError as error:
        raise HTTPException(status_code=401, detail=str(error))

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)

def get_me(current_user: User = Depends(get_current_user)):
    return current_user