from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.basic_jwt_user_auth import create_access_token
from app.exc.users import (
    InvalidCredentialsForLoginException,
    UserAlreadyExistsException,
)
from app.models import User
from app.schemas import JWTTokenDTO, UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAuth:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()

    async def sign_up_user(self, user: UserCreate) -> JWTTokenDTO:
        if await self.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email, password=hashed_password, username=user.username
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return JWTTokenDTO(access_token=create_access_token(data=user))

    async def login_user(self, user: UserLogin) -> JWTTokenDTO:
        db_user = await self.get_user_by_email(user.email)
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise InvalidCredentialsForLoginException()
        return JWTTokenDTO(access_token=create_access_token(data=user))
