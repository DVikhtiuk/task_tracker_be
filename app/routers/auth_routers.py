from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import logger
from app.db.database import get_db_session
from app.exc.users import InvalidCredentialsForLoginException, UserAlreadyExistsException
from app.schemas import JWTTokenDTO, UserCreate, UserLogin
from app.services.users_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=JWTTokenDTO)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_db_session)) -> JWTTokenDTO:
    """
    Registers a new user in the system.

    Args:
        user (UserCreate): The user data required to create a new account.
        session (AsyncSession): The SQLAlchemy asynchronous session dependency.

    Returns:
        JWTTokenDTO: The JWT token information for the newly created user.

    Raises:
        HTTPException:
            - 400: If the user already exists in the system.
            - 500: If an unexpected error occurs during user creation.
    """
    try:
        logger.info(f"Creating user with email: {user.email}")
        auth = UserService(session)
        result = await auth.sign_up_user(user=user)
        logger.info(f"User with email: '{user.email}' created successfully")
        return result
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", response_model=JWTTokenDTO, status_code=status.HTTP_200_OK)
async def login(
    user: UserLogin,
    session: AsyncSession = Depends(get_db_session),
) -> JWTTokenDTO:
    """
    Authenticates a user and returns a JWT token.

    Args:
        user (UserLogin): The user credentials for login.
        session (AsyncSession): The SQLAlchemy asynchronous session dependency.

    Returns:
        JWTTokenDTO: The JWT token information for the authenticated user.

    Raises:
        HTTPException:
            - 401: If the provided credentials are invalid.
            - 500: If an unexpected error occurs during user login.
    """
    try:
        logger.info(f"Try to logging in user with email: {user.email}")
        auth = UserService(session)
        result = await auth.login_user(user=user)
        logger.info(f"User with email: {user.email} logged in successfully")
        return result
    except InvalidCredentialsForLoginException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
