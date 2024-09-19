from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.user_role import UserRole
from app.types import intpk, when_created, when_updated


class User(Base):
    """
    Model representing a user in the system.

    Attributes:
        id (Mapped[intpk]): The primary key for the user.
        username (Mapped[str]): The username of the user (max length: 50 characters), must be unique.
        password (Mapped[str]): The hashed password of the user (max length: 255 characters).
        role (Mapped[UserRole]): The role of the user, defined by the `UserRole` enum. Defaults to `UserRole.USER`.
        email (Mapped[str]): The email of the user (max length: 100 characters), must be unique.
        created_at (Mapped[when_created]): The timestamp when the user was created.
        updated_at (Mapped[when_updated]): The timestamp when the user was last updated.
        tasks (Mapped[list["Task"]]): Relationship to the `Task` model representing the list of tasks the user is
         responsible for.
    """

    __tablename__ = "users"
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[when_created]
    updated_at: Mapped[when_updated]
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="responsible_person")
