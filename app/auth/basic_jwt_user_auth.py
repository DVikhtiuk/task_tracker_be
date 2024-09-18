from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.settings import settings
from app.db.database import get_db_session
from app.models import User
from app.schemas import UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

token_auth_scheme = HTTPBearer()


def create_access_token(
    data: UserCreate, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.model_dump().copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user_email_from_token(token: str = Depends(token_auth_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email


async def get_current_user(
    session: AsyncSession = Depends(get_db_session),
    current_user_email: str = Depends(get_current_user_email_from_token),
) -> UserResponse:
    if current_user_email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    current_user = (
        await session.execute(select(User).filter_by(email=current_user_email))
    ).scalar_one_or_none()
    if current_user is not None:
        return UserResponse(email=current_user.email, id=current_user.id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
