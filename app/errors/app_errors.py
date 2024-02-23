from typing import Optional


class V2xVirtualAdminError(Exception):
    """
    Base class for all V2X Virtual Admin Error exceptions.
    """

    def __init__(self, message: str = "", error_details: Optional[str] = None):
        """
        Init V2xVirtual Admin Error object.

        :param message: Error message, defaults to "".
        :param error_details: Additional error details messagem,
            defaults to None.
        """
        if error_details is None:
            error_details = message
        super(V2xVirtualAdminError, self).__init__(message)
        self.error_info = error_details


class DatastoreInitError(V2xVirtualAdminError):
    """
    A problem occurred during initialize datastore.
    """


class AdminUserCreateError(V2xVirtualAdminError):
    """
    A problem occurred during create admin user.
    """


class AdminRoleCreateError(V2xVirtualAdminError):
    """
    A problem occurred during create admin role.
    """


class UserFindError(V2xVirtualAdminError):
    """
    A problem occurred during find specified user from datastore.
    """
