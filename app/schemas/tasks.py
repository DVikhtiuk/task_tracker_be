from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.task_status import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: int
    status: TaskStatus = TaskStatus.TODO
    responsible_person_id: Optional[int]

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int]
    status: Optional[TaskStatus]

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
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
    tasks: list[TaskResponse]
    total: int
    limit: int
    offset: int


class TaskFilters(BaseModel):
    status: Optional[str] = None
    priority: Optional[int] = None
    responsible_person_id: Optional[int] = None


class Pagination(BaseModel):
    limit: int = Field(10, ge=1, le=100, description="Number of items per page (default is 10)")
    offset: int = Field(
        0,
        ge=0,
        description="The number of items to skip before starting to collect the result set",
    )
