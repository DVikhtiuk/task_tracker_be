from enum import StrEnum


class UserRole(StrEnum):
    """
    Enum class representing different user roles within the application.

    Attributes:
        ADMIN (str): Role with administrative privileges.
        USER (str): Standard user role with basic access.
        MANAGER (str): Role with managerial privileges, typically between user and admin.
    """

    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
