class UserAlreadyExistsException(Exception):
    """
    Exception raised when attempting to create a user that already exists.

    Attributes:
        message (str): The error message to be displayed.
    """

    def __init__(self, message: str = None):
        """
        Initializes the exception with an optional message.

        Args:
            message (str, optional): Custom error message. Defaults to "User with this email already exists.".
        """
        if message is None:
            message = "User with this email already exists."
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsForLoginException(Exception):
    """
    Exception raised when invalid credentials are provided during login.

    Attributes:
        message (str): The error message to be displayed.
    """

    def __init__(self, message: str = None):
        """
        Initializes the exception with an optional message.

        Args:
            message (str, optional): Custom error message. Defaults to "Invalid credentials were provided.
            Can't login.".
        """
        if message is None:
            message = "Invalid credentials were provided. Can't login."
        self.message = message
        super().__init__(self.message)


class UserPermissionsDeniedException(Exception):
    """
    Exception raised when a user attempts an action without the necessary permissions.

    Attributes:
        message (str): The error message to be displayed.
    """

    def __init__(self, message: str = None):
        """
        Initializes the exception with an optional message.

        Args:
            message (str, optional): Custom error message. Defaults to "Permission denied for current user.".
        """
        if message is None:
            message = "Permission denied for current user."
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """
    Exception raised when a user with a specified ID is not found.

    Attributes:
        user_id (int, optional): The ID of the user that was not found.
        message (str): The error message to be displayed.
    """

    def __init__(self, user_id: int = None, message: str = None):
        """
        Initializes the exception with the given user ID and an optional message.

        Args:
            user_id (int, optional): The ID of the user that was not found.
            message (str, optional): Custom error message. Defaults to "User with ID {user_id} not found."
            if user_id is provided, otherwise defaults to "User not found.".
        """
        if message is None:
            message = f"User with ID {user_id} not found." if user_id else "User not found."
        self.message = message
        super().__init__(self.message)
