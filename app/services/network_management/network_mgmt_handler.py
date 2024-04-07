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
    _summary_

    :param session: _description_
    """
    if session in STC_SESSION_PN_MAPPING:
        return STC_SESSION_PN_MAPPING.get(session, "")

    return ""


def build_ports_response(net_ifs: List[Ipv4NetworkInterface],
                         stc_ports: List[StcPort]
                         ) -> List[Dict[str, Dict[str, str]]]:
    """
    _summary_

    :param net_ifs: _description_
    :param stc_ports: _description_
    :return: _description_
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


def get_test_ports() -> List[Dict[str, Dict[str, str]]]:
    """
    _summary_

    :return: _description_
    """
    stc_obj = stchttp.StcHttp(STC_SERVER, port=STC_SERVER_PORT)
    sessions = stc_handler.list_sessions(stc_obj)

    if not sessions:
        return []

    part_num = get_part_num_by_session(sessions[0])
    stc_ports = stc_handler.get_stc_ports(stc_obj, sessions)
    net_ifs = net_if_models.get_network_interfaces(part_num)

    if stc_ports and net_ifs:
        return build_ports_response(net_ifs, stc_ports)

    return []
