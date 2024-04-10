from errors.app_errors import V2xVirtualAdminError


class StcError(V2xVirtualAdminError):
    """
    A problem occurred during the getting STC objects.
    """


class StcPortError(StcError):
    """
    A problem occurred during the getting STC port information.
    """


class StcSessionError(StcError):
    """
    A problem occurred during the getting or joining a STC session.
    """


class StcPhyError(StcError):
    """
    A problem occurred during the getting a STC Phy object.
    """


class StcPartNumError(StcError):
    """
    A problem occurred during the getting the STC part num.
    """
