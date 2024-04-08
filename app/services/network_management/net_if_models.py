import logging
import re
import subprocess
from typing import List, Optional

import errors.network_errors as if_errors
from const import APP_LOGGER, PN_PORT_MAPPING
from services.network_management.net_if_utils import (is_valid_ipv4,
                                                      netmask_to_ipv4_addr)

LOG = logging.getLogger(APP_LOGGER)


SLOT_PORT_REGEXP = re.compile(r"slot([\d]+)port([\d]+)")

IPV4_WITH_NETMASK_REGEXP = re.compile(
    r"inet ((25[0-5]|[1-2][0-4][0-9]|[1]?[1-9]?[0-9]).){3}" +
    r"(25[0-5]|[1-2][0-4][0-9]|[1]?[1-9]?[0-9])/([\d]+)")


class Ipv4NetworkInterface(object):
    """
    This class is used to store the IPv4 network interface information.
    """

    def __init__(self, name: str, address: str, gateway: str, netmask: str):
        self.__name = name
        self.__address = address
        self.__gateway = gateway
        self.__netmask = netmask

    @property
    def name(self) -> str:
        return self.__name

    @property
    def address(self) -> str:
        if is_valid_ipv4(self.__address):
            return self.__address
        msg = f"{self.__address} is invalid IPv4 Address."
        LOG.exception(msg)
        raise if_errors.InvalidIpv4AddressError(
            message=msg)

    @property
    def gateway(self) -> str:
        if self.__gateway == "" \
                or is_valid_ipv4(self.__gateway):
            return self.__gateway
        msg = f"{self.__gateway} is invalid IPv4 gateway."
        LOG.exception(msg)
        raise if_errors.InvalidIpv4AddressError(
            message=msg)

    @property
    def netmask(self) -> str:
        has_exception = False
        try:
            netmask = int(self.__netmask)
        except Exception:
            has_exception = True

        if has_exception or netmask not in range(0, 33):
            msg = f"{self.__netmask} is invalid netmask."
            LOG.exception(msg)
            raise if_errors.GettingNetworkInterfaceError(
                message=msg)

        return netmask_to_ipv4_addr(netmask)


def list_network_info() -> str:
    """
    List network interface infromation.

    :raises if_errors.GettingNetworkInterfaceError: A problem occurred
    when getting network interface information.
    :return: Network information.
    """
    ret = subprocess.run("ip address show", shell=True, capture_output=True)
    if ret.stderr:
        LOG.exception(ret.stderr.decode("utf-8"))
        raise if_errors.GettingNetworkInterfaceError(
            message=ret.stderr.decode("utf-8")
        )

    return ret.stdout.decode("utf-8")


def get_stc_network_interfaces(net_info: str) -> List[Ipv4NetworkInterface]:
    """
    Gets network interface infromation for STC test ports.

    :param net_info: A list of IPv4 network interface objects.
    """
    network_interfaces: List[Ipv4NetworkInterface] = []

    net_if_list = net_info.replace("\n ", " ").split("\n")
    for network_interface in net_if_list:
        net_interface = get_stc_network_interface(network_interface)
        if net_interface:
            network_interfaces.append(net_interface)

    return network_interfaces


def get_stc_network_interface(net_if: str) -> Optional[Ipv4NetworkInterface]:
    """
    Get IPv4 network interface information for STC test port.

    :param net_if: Network interface informatino.
    :return: Ipv4NetworkInterface object.
    """
    slot_port = SLOT_PORT_REGEXP.search(net_if)
    if slot_port is None:
        return None

    inet = IPV4_WITH_NETMASK_REGEXP.search(net_if)
    if inet is None:
        return None

    ipv4_addr, netmask = inet.group(0).replace("inet ", "").split("/")

    return Ipv4NetworkInterface(slot_port.group(0), ipv4_addr, "", netmask)


def list_ifs_by_part_num(part_number: str,
                         net_ifs: List[Ipv4NetworkInterface]
                         ) -> List[Ipv4NetworkInterface]:
    """
    List STC test port network interfaces by part num.

    :param part_number: Part number.
    :param net_ifs: List of Ipv4NetworkInterface objects.
    :return: The Ipv4NetworkInterface objects of STC test ports.
    """
    stc_net_ifs: List[Ipv4NetworkInterface] = []
    ports = PN_PORT_MAPPING.get(part_number, [])

    for net_if in net_ifs:
        print(net_if.name)
        if net_if.name in ports:
            stc_net_ifs.append(net_if)

    return stc_net_ifs


def get_network_interfaces(part_num: str) -> List[Ipv4NetworkInterface]:
    """
    Gets STC test port network interfaces.

    :param part_num: STC part num.
    :raises if_errors.NetworkInfoError: Failed to get network
    interface information.
    :return: A list of Ipv4NetworkInterface objects.
    """
    try:
        net_info = list_network_info()
        LOG.debug(f"Network interfaces:\n{net_info}")
        stc_net_interfaces = get_stc_network_interfaces(net_info)
        LOG.debug(f"STC network interfaces:\n{stc_net_interfaces}")
        network_interfaces = list_ifs_by_part_num(
            part_num, stc_net_interfaces)
        LOG.debug(f"STC test port interfaces:\n{network_interfaces}")

    except Exception as err:
        msg = 'Failed to get network interface information.'
        LOG.exception(f"{msg} {err}")
        raise if_errors.NetworkInfoError(
            message=msg,
            error_details=str(err)
        )

    return network_interfaces
