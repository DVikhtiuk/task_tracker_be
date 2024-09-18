from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.user_role import UserRole
from app.types import intpk, when_created, when_updated


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[when_created]
    updated_at: Mapped[when_updated]
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="responsible_person"
    )
