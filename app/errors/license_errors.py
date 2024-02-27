from errors.app_errors import V2xVirtualAdminError


class LicenseFileReadError(V2xVirtualAdminError):
    """
    A problem occurred during the reading of the V2X Virtual license file.
    """


class DateFormatError(V2xVirtualAdminError):
    """
    A problem occurred when the date string format has an error.
    """


class LicenseParseError(V2xVirtualAdminError):
    """
    A problem occurred during parsing the V2X Virtual license file content
    """
