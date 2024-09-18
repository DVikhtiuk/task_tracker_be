import datetime

from pydantic import BaseModel, EmailStr, constr

from app.enums.user_role import UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserCreate(UserLogin):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class JWTTokenDTO(BaseModel):
    access_token: str
