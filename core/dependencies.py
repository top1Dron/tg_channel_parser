from typing import Annotated

from django.conf import settings
from django.contrib.auth.models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt


ALGORITHM = "HS256"
OAUTH2_SCHEME = APIKeyHeader(name="Authorization", auto_error=False)


async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> User | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub", "")
        
        if not user_id_str:
            return None
        
        try:
            user = await User.objects.aget(id=user_id_str)
            return user
        except (User.DoesNotExist, ValueError):
            return None
    except JWTError:
        return None


async def get_current_active_user(user: Annotated[User | None, Depends(get_current_user)]) -> User:
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


async def get_superuser_user(user: Annotated[User | None, Depends(get_current_user)]) -> User:
    if not user or not user.is_active or not user.is_superuser:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user