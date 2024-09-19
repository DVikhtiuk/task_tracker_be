import datetime

from pydantic import BaseModel, EmailStr, constr

from app.enums.user_role import UserRole


class UserLogin(BaseModel):
    """
    Schema for user login information.

    Attributes:
        email (EmailStr): The email address of the user.
        password (constr): The password of the user, with a minimum length of 8 characters.
    """

    email: EmailStr
    password: constr(min_length=8)


class UserCreate(UserLogin):
    """
    Schema for creating a new user, inheriting from `UserLogin`.

    Attributes:
        username (str): The username of the new user.
    """

    username: str


class UserResponse(BaseModel):
    """
    Schema representing the response data for a user.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        role (UserRole): The role of the user in the system, defined by the `UserRole` enum.
        created_at (datetime.datetime): The timestamp when the user was created.
        updated_at (datetime.datetime): The timestamp when the user was last updated.
    """

    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class JWTTokenDTO(BaseModel):
    """
    Schema representing a JWT token.

    Attributes:
        access_token (str): The JWT access token string.
    """

    access_token: str
