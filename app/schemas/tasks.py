from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.task_status import TaskStatus


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Attributes:
        title (str): Title of the task.
        description (Optional[str]): Optional description of the task.
        priority (int): Priority level of the task.
        status (TaskStatus): Status of the task. Default is `TaskStatus.TODO`.
        responsible_person_id (Optional[int]): ID of the responsible person for the task.
    """

    title: str
    description: Optional[str]
    priority: int
    status: TaskStatus = TaskStatus.TODO
    responsible_person_id: Optional[int]

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Attributes:
        title (Optional[str]): New title of the task.
        description (Optional[str]): New description of the task.
        priority (Optional[int]): New priority level of the task.
        status (Optional[TaskStatus]): New status of the task.
    """

    title: Optional[str]
    description: Optional[str]
    priority: Optional[int]
    status: Optional[TaskStatus]

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    """
    Schema for returning detailed information about a task.

    Attributes:
        id (int): Unique identifier of the task.
        title (str): Title of the task.
        description (Optional[str]): Description of the task.
        priority (int): Priority level of the task.
        status (TaskStatus): Status of the task.
        responsible_person_id (int): ID of the responsible person for the task.
        created_at (datetime): Timestamp of task creation.
        updated_at (datetime): Timestamp of the last update.
    """

    id: int
    title: str
    description: Optional[str]
    priority: int
    status: TaskStatus
    responsible_person_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """
    Schema for returning a list of tasks with pagination details.

    Attributes:
        tasks (list[TaskResponse]): List of tasks.
        total (int): Total number of tasks matching the query.
        page (int): Current page number.
        page_size (int): Number of tasks per page.
    """

    tasks: list[TaskResponse]
    total: int
    page: int
    page_size: int


class TaskFilters(BaseModel):
    """
    Schema for applying filters to a list of tasks.

    Attributes:
        status (Optional[str]): Filter by task status.
        priority (Optional[int]): Filter by task priority.
        responsible_person_id (Optional[int]): Filter by responsible person ID.
    """

    status: Optional[str] = None
    priority: Optional[int] = None
    responsible_person_id: Optional[int] = None


class Pagination(BaseModel):
    """
    Schema for pagination parameters.

    Attributes:
        page (int): Current page number. Default is 1.
        page_size (int): Number of items per page. Default is 10.
    """

    page: int = Field(1, ge=1, description="Page number (default is 1)")
    page_size: int = Field(10, ge=1, le=100, description="Number of items per page (default is 10)")
