from errors.app_errors import V2xVirtualAdminError


class LicenseFileReadError(V2xVirtualAdminError):
    """
    A problem occurred during read V2X Virtual license file.
    """


class DateFormatError(V2xVirtualAdminError):
    """
    A problem occurred when date string format is error.
    """


class LicenseParseError(V2xVirtualAdminError):
    """
    A problem occurred during parse the V2X Virtual license file content.
    """
