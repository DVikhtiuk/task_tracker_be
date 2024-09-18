from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.tasks import Task
from app.models.users import User


class TaskExecutor(Base):
    __tablename__ = "task_executors"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    task: Mapped[Task] = relationship("Task", back_populates="executors")
    user: Mapped[User] = relationship("User")
