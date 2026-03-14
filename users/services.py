from typing import Annotated

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from fastapi import Depends, HTTPException
from jose import JWTError, jwt


class AuthService:
    """Service for handling authentication-related operations."""
    
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5
    REFRESH_TOKEN_EXPIRE_DAYS = 60

    def create_access_token(self, subject: str, exp_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        from datetime import datetime, timedelta
        expire = datetime.utcnow() + timedelta(minutes=exp_minutes)
        to_encode = {"sub": subject, "token_type": "access", "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_refresh_token(self, subject: str, exp_days: int = REFRESH_TOKEN_EXPIRE_DAYS) -> str:
        from datetime import datetime, timedelta
        expire = datetime.utcnow() + timedelta(days=exp_days)
        to_encode = {"sub": subject, "token_type": "refresh", "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM)