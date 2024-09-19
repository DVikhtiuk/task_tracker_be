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
from app.schemas import UserCreate, UserLogin, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

token_auth_scheme = HTTPBearer()


def create_access_token(data: UserCreate | UserLogin, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token based on the provided user data.

    Args:
        data (UserCreate | UserLogin): The user data to encode in the token.
        expires_delta (timedelta | None, optional): The token expiration time. If None, the token will expire
        after 15 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.model_dump().copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user_email_from_token(token=Depends(token_auth_scheme)) -> str:
    """
    Extracts and returns the current user's email from the JWT token.

    Args:
        token (Depends): The JWT token extracted from the request headers using HTTPBearer.

    Returns:
        str: The user's email extracted from the JWT token.

    Raises:
        HTTPException: If the token is invalid or the email is not found in the token payload.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
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
    """
    Retrieves the current user from the database based on the extracted email from the token.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session for database access.
        current_user_email (str): The current user's email extracted from the token.

    Returns:
        UserResponse: The user data formatted as a UserResponse schema.

    Raises:
        HTTPException: If the user is not found or the email is None.
    """
    if current_user_email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    current_user = (await session.execute(select(User).filter_by(email=current_user_email))).scalar_one_or_none()
    if current_user is not None:
        return UserResponse.from_orm(current_user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
