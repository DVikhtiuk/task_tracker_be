from enum import StrEnum


class TaskStatus(StrEnum):
    """
    Enum class representing the status of a task.

    Attributes:
        TODO (str): Represents a task that has not been started.
        IN_PROGRESS (str): Represents a task that is currently in progress.
        DONE (str): Represents a task that has been completed.
    """

    TODO = "TODO"
    IN_PROGRESS = "In progress"
    DONE = "Done"
