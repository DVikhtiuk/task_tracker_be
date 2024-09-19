from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.tasks import Task
from app.models.users import User


class TaskExecutor(Base):
    """
    Association table model representing the relationship between tasks and their executors.

    Attributes:
        task_id (Mapped[int]): The ID of the task. Part of the composite primary key.
        user_id (Mapped[int]): The ID of the user. Part of the composite primary key.
        task (Mapped[Task]): The relationship to the `Task` model, linking a task to its executors.
        user (Mapped[User]): The relationship to the `User` model, representing the user executing the task.
    """

    __tablename__ = "task_executors"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    task: Mapped[Task] = relationship("Task", back_populates="executors")
    user: Mapped[User] = relationship("User")
