import logging

from const import APP_LOGGER

LOG = logging.getLogger(APP_LOGGER)


def is_valid_ipv4(ip) -> bool:
    """
    Determines if the string value given as input is a valid IPv4 address.

    :param str ip: Probable IP.
    :return: True or False.
    """
    str_val = str(ip)
    ip_octets = str_val.split(".")
    if len(ip_octets) != 4:
        return False
    for octet in ip_octets:
        try:
            int(octet)
        except Exception:
            return False
        if int(octet) < 0 or int(octet) > 255:
            return False

    return True


def netmask_to_ipv4_addr(netmask_length: int) -> str:
    """
    Convert the netmask length to IPv4 address.

    :param netmask_length: Netmask length. The netmask length (0 - 32).
    :return: _description_
    """

    subnet_mask = (0xffffffff << (32 - netmask_length)) & 0xffffffff

    # Convert subnet mask to IP address format
    ip_address = ".".join(map(str, [(subnet_mask >> 24) & 0xff,
                                    (subnet_mask >> 16) & 0xff,
                                    (subnet_mask >> 8) & 0xff,
                                    subnet_mask & 0xff]))

    return ip_address
