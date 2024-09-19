from app.enums.user_role import UserRole
from app.exc.users import UserPermissionsDeniedException
from app.models import Task, User


def check_user_permissions_for_task_creation(current_user: User, responsible_person: User, task: Task) -> None:
    """
    Validates if the current user has the necessary permissions to create a task.

    Args:
        current_user (User): The user attempting to create the task.
        responsible_person (User): The user assigned as the responsible person for the task.
        task (Task): The task object being created.

    Raises:
        UserPermissionsDeniedException: If the current user does not have permission to create the task.
    """
    if current_user.role == UserRole.USER and not (
        task.responsible_person_id == current_user.id or current_user in task.executors
    ):
        raise UserPermissionsDeniedException()
    elif current_user.role == UserRole.MANAGER and responsible_person.role == UserRole.ADMIN:
        raise UserPermissionsDeniedException(message="Permission denied. Manager can't apply task for administrator")
    elif current_user.role == UserRole.USER and current_user.id != responsible_person.id:
        raise UserPermissionsDeniedException(
            message="Permission denied. User can't apply task for other users, managers, and administrators"
        )


def check_user_permissions_for_task_access(current_user: User, task: Task) -> None:
    """
    Validates if the current user has the necessary permissions to access a task.

    Args:
        current_user (User): The user attempting to access the task.
        task (Task): The task object being accessed.

    Raises:
        UserPermissionsDeniedException: If the current user does not have permission to access the task.
    """
    if current_user.role in {UserRole.USER, UserRole.MANAGER}:
        if task.responsible_person_id != current_user.id and current_user not in task.executors:
            raise UserPermissionsDeniedException(
                message="Permission denied. Users and Managers can only access their own tasks."
            )


def check_user_permissions_for_task_delete(current_user: User, task: Task) -> None:
    """
    Validates if the current user has the necessary permissions to delete a task.

    Args:
        current_user (User): The user attempting to delete the task.
        task (Task): The task object being deleted.

    Raises:
        UserPermissionsDeniedException: If the current user does not have permission to delete the task.
    """
    if current_user.role == UserRole.MANAGER:
        if task.responsible_person_id != current_user.id and current_user not in task.executors:
            raise UserPermissionsDeniedException(
                message="Managers can only delete tasks they are responsible for or involved in."
            )

    elif current_user.role == UserRole.USER:
        if task.responsible_person_id != current_user.id:
            raise UserPermissionsDeniedException(message="Users can only delete tasks they are responsible for.")
