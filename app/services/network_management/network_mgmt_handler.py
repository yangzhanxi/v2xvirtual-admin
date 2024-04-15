import logging
from typing import Dict, List

from stcrestclient import stchttp

from const import (APP_LOGGER, STC_SERVER, STC_SERVER_PORT,
                   STC_SESSION_PN_MAPPING)
from services.network_management import net_if_models, stc_handler
from services.network_management.net_if_models import Ipv4NetworkInterface
from services.network_management.stc_handler import StcPort

LOG = logging.getLogger(APP_LOGGER)


def get_part_num_by_session(session: str) -> str:
    """
    Gets part num by the name of STC session.

    :param session: The name of STC session.
    """
    if session in STC_SESSION_PN_MAPPING:
        return STC_SESSION_PN_MAPPING.get(session, "")

    return ""


def build_ports_response(net_ifs: List[Ipv4NetworkInterface],
                         stc_ports: List[StcPort]
                         ) -> List[Dict[str, Dict[str, str]]]:
    """
    Construct the response of ports request.

    :param net_ifs: A list of Ipv4NetworkInterface objects.
    :param stc_ports: A list of StcPort objects.
    :return: A list of STC network interface information.
    """
    ports = []
    for net_if in net_ifs:
        for stc_port in stc_ports:
            if net_if.name == stc_port.name:
                port_info = {
                    "port_name": {
                        "label": "Port Name",
                        "value": net_if.name
                    },
                    "port_handel": {
                        "label": "Port Handel",
                        "value": stc_port.handle
                    },
                    "link_status": {
                        "label": "Link Status",
                        "value": stc_port.link_status
                    },
                    "line_speed": {
                        "label": "Line Speed",
                        "value": stc_port.line_speed
                    },
                    "auto_negotiation": {
                        "label": "Auto-Negotiation",
                        "value": stc_port.auto_negotiation
                    },
                    "auto_negotiation_role": {
                        "label": "Auto-Negotiation Role",
                        "value": stc_port.auto_negotiation_role
                    },
                    "duplex_mode": {
                        "label": "Duplex Mode",
                        "value": stc_port.duplex_mode
                    },
                    "ip_version": {
                        "label": "IP version",
                        "value": "IPv4"
                    },
                    "address": {
                        "label": "IP Address",
                        "value": net_if.address
                    },
                    "netmask": {
                        "label": "Netmask",
                        "value": net_if.netmask
                    },
                    "gateway": {
                        "label": "Gateway",
                        "value": net_if.gateway
                    }
                }
                ports.append(port_info)

    return ports


def ports_handler() -> List[Dict[str, Dict[str, str]]]:
    """
    This method serves as the handler for STC ports,
    responsible for processing port requests.

    :return: Response of ports request.
    """
    try:
        stc_obj = stchttp.StcHttp(STC_SERVER, port=STC_SERVER_PORT)
        sessions = stc_handler.list_sessions(stc_obj)
        if not sessions:
            return []

        stc_ports = stc_handler.get_stc_ports(stc_obj, sessions)
        part_num = stc_handler.get_part_num(stc_obj)
        net_ifs = net_if_models.get_network_interfaces(part_num)

        if stc_ports and net_ifs:
            return build_ports_response(net_ifs, stc_ports)

    except Exception as err:
        msg = str(err)
        if hasattr(err, "error_info"):
            if err.error_info != msg:
                msg = f"{msg} {err.error_info}"
        LOG.exception(msg)

    return []


def part_num_handler() -> Dict[str, str]:
    """
    This method serves as the handler for STC part num,
    responsible for processing part num requests.

    :return: Response of part num.
    """
    def_ret = {"part_num": ""}
    try:
        stc_obj = stchttp.StcHttp(STC_SERVER, port=STC_SERVER_PORT)
        sessions = stc_handler.list_sessions(stc_obj)
        if not sessions:
            return def_ret

        stc_handler.join_session(stc_obj, sessions[0])
        part_num = stc_handler.get_part_num(stc_obj)

        return {"part_num": part_num}

    except Exception as err:
        msg = str(err)
        if hasattr(err, "error_info"):
            msg = f"{msg} {err.error_info}"
        LOG.exception(msg)

    return def_ret
