from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.settings import logger
from app.enums.user_role import UserRole
from app.exc.tasks import TaskNotFoundException
from app.models import Task, User
from app.schemas.tasks import Pagination, TaskCreate, TaskFilters, TaskListResponse, TaskResponse, TaskUpdate
from app.services.email_service import EmailService
from app.utils.tasks_utils import check_filters_data, check_task_priority, get_user_by_id_or_404
from app.utils.user_permissions_check import (
    check_user_permissions_for_task_access,
    check_user_permissions_for_task_creation,
    check_user_permissions_for_task_delete,
)


class TaskService:
    """
    Service class for managing tasks. Provides methods to create, retrieve, update,
    and delete tasks, as well as handle task-related operations such as sending notifications.

    Attributes:
        session (AsyncSession): The SQLAlchemy session used for database operations.
        email_service (EmailService): Service used for sending email notifications.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the TaskService with a database session and sets up the email service.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        self.session = session
        self.email_service = EmailService(logger=logger)

    async def create_task(self, task_data: TaskCreate, current_user: User) -> TaskResponse:
        """
        Creates a new task in the database.

        Args:
            task_data (TaskCreate): The data required to create a new task.
            current_user (User): The user creating the task.

        Returns:
            TaskResponse: The created task details.

        Raises:
            InvalidTaskPriorityException: If the task priority is not valid.
            UserNotFoundException: If the responsible user is not found.
            UserPermissionsDeniedException: If the user does not have permission to create the task.
        """
        check_task_priority(task_data.priority)
        responsible_person = await get_user_by_id_or_404(user_id=task_data.responsible_person_id, session=self.session)
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=task_data.status,
            responsible_person_id=current_user.id
            if current_user.role == UserRole.USER
            else task_data.responsible_person_id,
        )
        check_user_permissions_for_task_creation(current_user, responsible_person, new_task)
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        return TaskResponse.from_orm(new_task)

    async def get_task_by_id_or_404(self, task_id: int) -> Task:
        """
        Retrieves a task by its ID or raises a 404 error if not found.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Task: The task object.

        Raises:
            TaskNotFoundException: If the task is not found.
        """
        result = await self.session.execute(
            select(Task).options(selectinload(Task.executors)).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return task

    async def get_task_by_id(self, task_id: int, current_user: User) -> TaskResponse:
        """
        Retrieves a task by its ID and checks if the current user has access to it.

        Args:
            task_id (int): The ID of the task to retrieve.
            current_user (User): The user requesting the task.

        Returns:
            TaskResponse: The task details.

        Raises:
            TaskNotFoundException: If the task is not found.
            UserPermissionsDeniedException: If the user does not have permission to access the task.
        """
        task = await self.get_task_by_id_or_404(task_id)
        check_user_permissions_for_task_access(current_user, task)
        return TaskResponse.from_orm(task)

    async def update_fields(self, task_data: TaskUpdate, task: Task) -> Task:
        """
        Update task fields and send email notification if status changes.

        Args:
            task_data (TaskUpdate): The data to update in the task.
            task (Task): The task object to update.

        Returns:
            Task: The updated task object.
        """
        old_status = task.status
        task = self.update_task_fields(task, task_data)

        if self.is_status_changed(old_status, task_data):
            responsible_person = await self.get_responsible_person(task.responsible_person_id)
            await self.send_status_change_notification(
                task, responsible_person, task_data.status, old_status=old_status
            )

        return task

    @staticmethod
    def update_task_fields(task: Task, task_data: TaskUpdate) -> Task:
        """
        Update the task fields with the provided data.

        Args:
            task (Task): The task to update.
            task_data (TaskUpdate): The new data for the task.

        Returns:
            Task: The updated task object.
        """
        update_fields = task_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(task, field, value)
        return task

    @staticmethod
    def is_status_changed(old_status: str, task_data: TaskUpdate) -> bool:
        """
        Check if the status of the task has changed.

        Args:
            old_status (str): The old status of the task.
            task_data (TaskUpdate): The new data for the task.

        Returns:
            bool: True if the status has changed, otherwise False.
        """
        new_status = task_data.status
        return new_status is not None and new_status != old_status

    async def get_responsible_person(self, user_id: int) -> User:
        """
        Retrieve the responsible person from the database.

        Args:
            user_id (int): The ID of the responsible person.

        Returns:
            User: The user object.

        Raises:
            UserNotFoundException: If the user is not found.
        """
        return await get_user_by_id_or_404(user_id=user_id, session=self.session)

    async def send_status_change_notification(
        self, task: Task, responsible_person: User, new_status: str, old_status: str
    ) -> None:
        """
        Send an email notification to the responsible person if the task status changes.

        Args:
            task (Task): The task object.
            responsible_person (User): The user to notify.
            new_status (str): The new status of the task.
            old_status (str): The old status of the task.
        """
        self.email_service.send_status_change_email(
            to_email=responsible_person.email,
            task_title=task.title,
            old_status=old_status,
            new_status=new_status,
        )

    async def update_task(self, task_id: int, task_data: TaskUpdate, current_user: User) -> TaskResponse:
        """
        Updates a specific task by its ID.

        Args:
            task_id (int): The ID of the task to update.
            task_data (TaskUpdate): The updated data for the task.
            current_user (User): The user requesting the update.

        Returns:
            TaskResponse: The updated task details.

        Raises:
            TaskNotFoundException: If the task is not found.
            UserPermissionsDeniedException: If the user does not have permission to update the task.
            InvalidTaskPriorityException: If the task priority is not valid.
        """
        task = await self.get_task_by_id_or_404(task_id)
        check_user_permissions_for_task_access(current_user, task)
        check_task_priority(task_data.priority)
        task = await self.update_fields(task_data, task)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return TaskResponse.from_orm(task)

    async def delete_task(self, task_id: int, current_user: User) -> TaskResponse:
        """
        Deletes a specific task by its ID.

        Args:
            task_id (int): The ID of the task to delete.
            current_user (User): The user requesting the deletion.

        Returns:
            TaskResponse: The details of the deleted task.

        Raises:
            TaskNotFoundException: If the task is not found.
            UserPermissionsDeniedException: If the user does not have permission to delete the task.
        """
        task = await self.get_task_by_id_or_404(task_id)
        check_user_permissions_for_task_delete(task=task, current_user=current_user)
        await self.session.delete(task)
        await self.session.commit()
        return TaskResponse.from_orm(task)

    @staticmethod
    def apply_filters(query, filters: TaskFilters) -> None:
        """
        Apply filters to the query for retrieving tasks.

        Args:
            query: The initial SQLAlchemy query object.
            filters (TaskFilters): The filters to apply.

        Returns:
            query: The modified query with the applied filters.
        """
        if filters.status:
            query = query.where(Task.status == filters.status)

        if filters.priority is not None:
            query = query.where(Task.priority == filters.priority)

        if filters.responsible_person_id:
            query = query.where(Task.responsible_person_id == filters.responsible_person_id)

        return query

    @staticmethod
    def apply_user_access_filter(query, current_user: User):
        """
        Apply user access restrictions to the query based on the user's role.

        Args:
            query: The initial SQLAlchemy query object.
            current_user (User): The user requesting the data.

        Returns:
            query: The modified query with access restrictions.
        """
        if current_user.role in {UserRole.USER, UserRole.MANAGER}:
            query = query.where(
                (Task.responsible_person_id == current_user.id) | Task.executors.any(User.id == current_user.id)
            )
        return query

    async def build_query(self, filters: TaskFilters, pagination: Pagination, current_user: User):
        """
        Build the query for retrieving tasks based on filters, pagination, and user access.

        Args:
            filters (TaskFilters): Filters to apply to the query.
            pagination (Pagination): Pagination parameters for the query.
            current_user (User): The user requesting the data.

        Returns:
            tuple: The query object and total count of tasks.
        """
        query = self.apply_user_access_filter(
            self.apply_filters(select(Task).options(selectinload(Task.executors)), filters),
            current_user,
        )
        total_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.execute(total_query)).scalar()

        query = query.limit(pagination.limit).offset(pagination.offset)
        return query, total

    async def get_tasks(self, filters: TaskFilters, pagination: Pagination, current_user: User) -> TaskListResponse:
        """
        Retrieves a list of tasks based on filters and pagination.

        Args:
            filters (TaskFilters): Filters to apply to the task list.
            pagination (Pagination): Pagination parameters for the task list.
            current_user (User): The user requesting the data.

        Returns:
            TaskListResponse: The list of tasks and pagination info.

        Raises:
            HTTPException: Errors related to user not found and server issues.
        """
        await check_filters_data(filters, self.session)
        query, total = await self.build_query(filters, pagination, current_user)
        result = await self.session.execute(query)
        tasks = result.scalars().all()

        return TaskListResponse(
            tasks=[TaskResponse.from_orm(task) for task in tasks],
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )
