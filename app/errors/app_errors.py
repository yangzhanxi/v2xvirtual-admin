from typing import Optional


class V2xVirtualAdminError(Exception):
    """
    Base class for all V2X Virtual Admin Error exceptions.
    """

    def __init__(self, message: str = "", error_details: Optional[str] = None):
        """
        Init V2xVirtual Admin Error object.

        :param message: Error message, defaults to "".
        :param error_details: Additional error details message,
            defaults to None.
        """
        if error_details is None:
            error_details = message
        super(V2xVirtualAdminError, self).__init__(message)
        self.error_info = error_details


class DatastoreInitError(V2xVirtualAdminError):
    """
    An issue occurred during the initialization of the datastore.
    """


class AdminUserCreateError(V2xVirtualAdminError):
    """
    A problem occurred during the creation of the admin user.
    """


class AdminRoleCreateError(V2xVirtualAdminError):
    """
    A problem occurred during the creation of the admin role.
    """


class UserFindError(V2xVirtualAdminError):
    """
    A problem occurred during the search for
    the specified user in the datastore.
    """


class LoggingConfigurationError(V2xVirtualAdminError):
    """
    A problem occurred during configuration logging.
    """
