from typing import Annotated
import os
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, APIRouter, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.dependencies import get_current_active_user
from users.schemas import LoginResponse, UserProfile
from users.services import AuthService


user_router = APIRouter()


# Get SECRET_KEY from Django settings (environment variable)
SECRET_KEY = getattr(django_settings, 'SECRET_KEY', os.getenv("DJANGO_SECRET_KEY"))
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is required")

ALGORITHM = "HS256"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/login")


@user_router.post("/register", tags=["auth"])
async def register(username: str, email: str, password: str):
    hashed = make_password(password)
    
    existing = User.objects.filter(Q(username=username) | Q(email=email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username or email already exists")
    
    user = await User.objects.acreate(
        username=username,
        email=email,
        password_hash=hashed
    )
    
    return {"id": str(user.id), "username": user.username, "email": user.email}


@user_router.post("/login", response_model=LoginResponse, tags=["auth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await User.objects.filter(username=form_data.username).afirst()
    if not user or not check_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth_service = AuthService()
    access = auth_service.create_access_token(str(user.id))
    refresh = auth_service.create_refresh_token(str(user.id))
    
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user_id": int(user.id),
        "username": user.username,
        "email": user.email
    }


@user_router.get("/user", response_model=UserProfile, tags=["auth"])
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


@user_router.post("/logout", tags=["auth"])
async def logout(refresh_token: str = Header(...), access_token: str = Header(...)):
    try:
        payload_access = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        payload_refresh = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"detail": "Logged out successfully", "tokens_invalidated": True}
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token(s): {str(e)}")
