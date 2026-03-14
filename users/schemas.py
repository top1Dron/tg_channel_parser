from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    confirm_password: str


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    
    @field_validator('confirm_password')
    def passwords_match(cls, v: str, info) -> str:
        user_data = info.data
        if user_data['password'] != v:
            raise ValueError('Passwords do not match')
        return v


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    email: EmailStr


class UserProfile(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True


class UserResponse(UserProfile):
    created_at: datetime
    updated_at: datetime
