from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exc.tasks import InvalidResponsiblePersonDataException, InvalidTaskPriorityException
from app.exc.users import UserNotFoundException
from app.models import User
from app.schemas.tasks import TaskFilters


def check_task_priority(priority: int) -> None:
    """
    Validates if the given task priority is within the acceptable range (0 to 3).

    Args:
        priority (int): The priority of the task to be checked.

    Raises:
        InvalidTaskPriorityException: If the priority is outside the range of 0 to 3.
    """
    if not (0 <= priority <= 3):
        raise InvalidTaskPriorityException(priority=priority)


def check_responsible_person_id(person_id: int) -> None:
    """
    Validates the responsible person's ID.

    Args:
        person_id (int): The ID of the responsible person to be validated.

    Raises:
        InvalidTaskDataException: If the provided person_id is less than or equal to zero.

    """
    if not (0 < person_id):
        raise InvalidResponsiblePersonDataException(person_id)


async def get_user_by_id_or_404(session: AsyncSession, user_id: int) -> User:
    """
    Retrieves a user by ID or raises a 404 exception if not found.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found.

    Raises:
        UserNotFoundException: If no user is found with the given ID.
    """
    result = await session.execute(select(User).filter_by(id=user_id))
    responsible_person = result.scalar_one_or_none()
    if not responsible_person:
        raise UserNotFoundException(user_id=user_id)
    return responsible_person


async def check_filters_data(filters: TaskFilters, session: AsyncSession) -> None:
    """
    Validates the provided task filters by checking the existence of users and the validity of task priority.

    Args:
        filters (TaskFilters): The filters provided for querying tasks.
        session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.

    Raises:
        UserNotFoundException: If the responsible person ID in the filters is not found.
        InvalidTaskPriorityException: If the priority in the filters is not within the acceptable range.
    """
    if filters.responsible_person_id:
        await get_user_by_id_or_404(user_id=filters.responsible_person_id, session=session)
    if filters.priority is not None:
        check_task_priority(filters.priority)
