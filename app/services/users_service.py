from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.basic_jwt_user_auth import create_access_token, pwd_context
from app.exc.users import InvalidCredentialsForLoginException, UserAlreadyExistsException
from app.models import User
from app.schemas import JWTTokenDTO, UserCreate, UserLogin


class UserService:
    """
    Service class for managing user operations such as sign up, login, and retrieval of user data.

    Attributes:
        session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the UserService with a database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        self.session = session

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User: The user object if found, or None if no user exists with the provided email.
        """
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()

    async def sign_up_user(self, user: UserCreate) -> JWTTokenDTO:
        """
        Registers a new user in the system.

        Args:
            user (UserCreate): The data required to create a new user.

        Returns:
            JWTTokenDTO: A JWT token for the newly created user.

        Raises:
            UserAlreadyExistsException: If a user with the provided email already exists.
        """
        if await self.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        hashed_password = pwd_context.hash(user.password)
        db_user = User(email=user.email, password=hashed_password, username=user.username)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return JWTTokenDTO(access_token=create_access_token(data=user))

    async def login_user(self, user: UserLogin) -> JWTTokenDTO:
        """
        Authenticates a user and generates a JWT token if successful.

        Args:
            user (UserLogin): The user credentials for login.

        Returns:
            JWTTokenDTO: A JWT token for the authenticated user.

        Raises:
            InvalidCredentialsForLoginException: If the provided credentials are invalid.
        """
        db_user = await self.get_user_by_email(user.email)
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise InvalidCredentialsForLoginException()
        return JWTTokenDTO(access_token=create_access_token(data=user))
