from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.task_status import TaskStatus
from app.models.users import User
from app.types import intpk, when_created, when_updated


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.TODO
    )
    created_at: Mapped[when_created]
    updated_at: Mapped[when_updated]
    responsible_person_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    responsible_person: Mapped[User] = relationship("User", back_populates="tasks")

    executors: Mapped[list["TaskExecutor"]] = relationship(
        "TaskExecutor", back_populates="task"
    )
