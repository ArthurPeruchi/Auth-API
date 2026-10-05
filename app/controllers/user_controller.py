from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserUpdate, UserCreate, UserResponse, UserPatch
from app.usecases.user_usecase import UserUseCase, UserNotFoundError, EmailAlreadyExistsError
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from app.infrastructure.security.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_usecase(db: Session = Depends(get_db)) -> UserUseCase:
    repository = UserRepository(db)
    password_hasher = Argon2PasswordHasher()

    return UserUseCase(repository, password_hasher)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)

def create_user(data: UserCreate, usecase: UserUseCase = Depends(get_user_usecase)):
    try:
        return usecase.create(data)

    except EmailAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))

@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)

def update_me(data: UserUpdate, current_user: User = Depends(get_current_user), usecase: UserUseCase = Depends(get_user_usecase)):
    try:
        return usecase.update(current_user.id, data)

    except UserNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except EmailAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))

@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)

def patch_me(data: UserPatch, current_user: User = Depends(get_current_user), usecase: UserUseCase = Depends(get_user_usecase)):
    try:
        return usecase.patch(current_user.id, data)
    
    except UserNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    
    except EmailAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))