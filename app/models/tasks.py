from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.task_status import TaskStatus
from app.models.users import User
from app.types import intpk, when_created, when_updated


class Task(Base):
    """
    Model representing a task in the system.

    Attributes:
        id (Mapped[intpk]): The primary key for the task.
        title (Mapped[str]): The title of the task (max length: 100 characters).
        description (Mapped[str]): A brief description of the task (max length: 500 characters), can be null.
        priority (Mapped[int]): The priority level of the task, must be provided.
        status (Mapped[TaskStatus]): The current status of the task. Defaults to `TaskStatus.TODO`.
        created_at (Mapped[when_created]): The timestamp when the task was created.
        updated_at (Mapped[when_updated]): The timestamp when the task was last updated.
        responsible_person_id (Mapped[int]): Foreign key linking to the user responsible for the task.
        responsible_person (Mapped[User]): Relationship to the `User` model representing the person responsible
        for the task. executors (Mapped[list["TaskExecutor"]]): Relationship to the `TaskExecutor` model representing
       the list of executors assigned to the task.
    """

    __tablename__ = "tasks"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    created_at: Mapped[when_created]
    updated_at: Mapped[when_updated]
    responsible_person_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    responsible_person: Mapped[User] = relationship("User", back_populates="tasks")

    executors: Mapped[list["TaskExecutor"]] = relationship("TaskExecutor", back_populates="task")
