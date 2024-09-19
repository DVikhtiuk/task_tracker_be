from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.basic_jwt_user_auth import get_current_user
from app.core.settings import logger
from app.db.database import get_db_session
from app.exc.tasks import InvalidResponsiblePersonDataException, InvalidTaskPriorityException, TaskNotFoundException
from app.exc.users import UserNotFoundException, UserPermissionsDeniedException
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.tasks import Pagination, TaskFilters, TaskListResponse
from app.services.tasks_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> TaskResponse:
    """
    Creates a new task in the system.

    Args:
        task_data (TaskCreate): The data required to create a new task.
        session (AsyncSession): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        TaskResponse: The response model containing the created task details.

    Raises:
        HTTPException: Various errors related to task creation, user permissions, and server issues.
    """
    logger.info(f"Create task requested by user: {current_user.id} with data: {task_data}")
    try:
        task_service = TaskService(session)
        result = await task_service.create_task(task_data, current_user)
        logger.info(f"Task created successfully: {result.id}")
        return result
    except (InvalidTaskPriorityException, UserPermissionsDeniedException, InvalidResponsiblePersonDataException) as e:
        logger.warning(f"Error during task creation: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except UserNotFoundException as e:
        logger.warning(f"User not found: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        logger.error(f"Unhandled exception during task creation: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> TaskResponse:
    """
    Retrieves a specific task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.
        session (AsyncSession): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        TaskResponse: The response model containing the task details.

    Raises:
        HTTPException: Errors related to task not found, user permissions, and server issues.
    """
    logger.info(f"Get task requested by user: {current_user.id} for task ID: {task_id}")
    try:
        task_service = TaskService(session)
        result = await task_service.get_task_by_id(task_id, current_user=current_user)
        logger.info(f"Task retrieved successfully: {result.id}")
        return result
    except TaskNotFoundException as e:
        logger.warning(f"Task not found: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserPermissionsDeniedException as e:
        logger.warning(f"Permission denied: {e.message}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except Exception as e:
        logger.error(f"Unhandled exception during task retrieval: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> TaskResponse:
    """
    Updates a specific task by its ID.

    Args:
        task_id (int): The ID of the task to update.
        task_data (TaskUpdate): The updated task data.
        session (AsyncSession): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        TaskResponse: The response model containing the updated task details.

    Raises:
        HTTPException: Errors related to task not found, user permissions, invalid priority, and server issues.
    """
    logger.info(f"Update task requested by user: {current_user.id} for task ID: {task_id} with data: {task_data}")
    try:
        task_service = TaskService(session)
        result = await task_service.update_task(task_id, task_data, current_user)
        logger.info(f"Task updated successfully: {result.id}")
        return result
    except (TaskNotFoundException, UserNotFoundException) as e:
        logger.warning(f"Task not found: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserPermissionsDeniedException as e:
        logger.warning(f"Permission denied: {e.message}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except InvalidTaskPriorityException as e:
        logger.warning(f"Invalid priority: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.error(f"Unhandled exception during task update: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{task_id}", response_model=TaskResponse)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> TaskResponse:
    """
    Deletes a specific task by its ID.

    Args:
        task_id (int): The ID of the task to delete.
        session (AsyncSession): The database session dependency.
        current_user: The currently authenticated user.

    Returns:
        TaskResponse: The response model containing the details of the deleted task.

    Raises:
        HTTPException: Errors related to task not found, user permissions, and server issues.
    """
    logger.info(f"Delete task requested by user: {current_user.id} for task ID: {task_id}")
    try:
        task_service = TaskService(session)
        result = await task_service.delete_task(task_id, current_user)
        logger.info(f"Task deleted successfully: {task_id}")
        return result
    except TaskNotFoundException as e:
        logger.warning(f"Task not found: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserPermissionsDeniedException as e:
        logger.warning(f"Permission denied: {e.message}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except Exception as e:
        logger.error(f"Unhandled exception during task deletion: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
    filters: TaskFilters = Depends(),
    pagination: Pagination = Depends(),
) -> TaskListResponse:
    """
    Retrieves a list of tasks based on filters and pagination.

    Args:
        session (AsyncSession): The database session dependency.
        current_user: The currently authenticated user.
        filters (TaskFilters): Filters to apply to the task list.
        pagination (Pagination): Pagination parameters for the task list.

    Returns:
        TaskListResponse: A response model containing a list of tasks and pagination info.

    Raises:
        HTTPException: Errors related to user not found and server issues.
    """
    logger.info(f"List tasks requested by user: {current_user.id} with filters: {filters}")
    try:
        task_service = TaskService(session)
        result = await task_service.get_tasks(filters=filters, current_user=current_user, pagination=pagination)
        logger.info(f"Tasks retrieved successfully, total: {len(result.tasks)}")
        return result
    except UserNotFoundException as e:
        logger.warning(f"User not found: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        logger.error(f"Unhandled exception during task listing: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
