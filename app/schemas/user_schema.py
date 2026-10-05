from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str

class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=5, max_length=100)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True