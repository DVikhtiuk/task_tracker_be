class TaskNotFoundException(Exception):
    """
    Exception raised when a task with the specified ID is not found.

    Attributes:
        task_id (int): The ID of the task that was not found.
        message (str): The error message to be displayed.
    """

    def __init__(self, task_id: int, message: str = None):
        """
        Initializes the exception with the given task ID and an optional message.

        Args:
            task_id (int): The ID of the task that was not found.
            message (str, optional): Custom error message. Defaults to "Task with ID {task_id} was not found.".
        """
        if message is None:
            message = f"Task with ID {task_id} was not found."
        self.message = message
        super().__init__(self.message)


class InvalidTaskPriorityException(Exception):
    """
    Exception raised when an invalid priority is assigned to a task.

    Attributes:
        priority (int): The invalid priority value.
        message (str): The error message to be displayed.
    """

    def __init__(self, priority: int, message: str = None):
        """
        Initializes the exception with the given priority and an optional message.

        Args:
            priority (int): The invalid priority value.
            message (str, optional): Custom error message. Defaults to "Invalid priority {priority}.
            Priority must be between 0 and 3.".
        """
        if message is None:
            message = f"Invalid priority {priority}. Priority must be between 0 and 3."
        self.message = message
        super().__init__(self.message)
