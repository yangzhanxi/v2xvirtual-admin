from errors.app_errors import V2xVirtualAdminError


class NetworkInfoError(V2xVirtualAdminError):
    """
    A problem occurred during the getting network interface information.
    """


class InvalidIpv4AddressError(NetworkInfoError):
    """
    Invalid IPv4 address.
    """


class InvalidIpv4NetmaskLenght(NetworkInfoError):
    """
    Invalid IPv4 netmask.
    """


class GettingNetworkInterfaceError(NetworkInfoError):
    """
    A problem occurred when getting network interface information.
    """
