import logging
from typing import List, Dict

from errors.stc_errors import StcPortError
from services.network_management.stc_port_models import StcPort
from const import STC_SESSION_PREFIX, STC_SESSION_SUFFIX, APP_LOGGER
from stcrestclient import stchttp

LOG = logging.getLogger(APP_LOGGER)


def list_sessions(stc: stchttp.StcHttp) -> List[str]:
    """
    _summary_
    """
    stc_sessions = stc.sessions()

    return stc_sessions


def join_session(stc: stchttp.StcHttp, session_name: str) -> None:
    """
    _summary_

    :param stc: _description_
    :param session_name: _description_
    """
    stc.join_session(session_name)


def list_ports(stc: stchttp.StcHttp) -> List[str]:
    """
    _summary_

    :param stc: _description_
    :return: _description_
    """
    ret = stc.get("project1", "children-port")
    if isinstance(ret, str):
        return [ret]

    return ret


def get_port_attributes(stc: stchttp.StcHttp, port_handle: str) -> Dict[str]:
    """
    _summary_

    :param stc: _description_
    :param port_handle: _description_
    """
    return stc.get(port_handle)


def get_ethernet_copper_handle(stc: stchttp.StcHttp,
                               port_handle: str) -> str:
    """
    _summary_

    :param stc: _description_
    :param port_handle: _description_
    """
    ret = stc.get(port_handle, "activephy-Targets")
    if isinstance(ret, str) and "ethernetcopper" in ret:
        return ret
    if isinstance(ret, list):
        for stc_object in ret:
            if "ethernetcopper" in stc_object:
                return stc_object

    return ""


def get_ethernet_copper_info(stc: stchttp.StcHttp,
                             eth_copper_handle: str) -> Dict[str]:
    """
    _summary_

    :param stc: _description_
    :param eth_copper_handle: _description_
    """
    ethernet_copper = stc.get(eth_copper_handle)

    return ethernet_copper


def get_eth_copper_handle_by_port_attr(port_info: dict) -> Dict[str]:
    """
    _summary_

    :param port_info: _description_
    """
    active_phy_targets = port_info.get("activephy-Targets")
    if isinstance(active_phy_targets, list):
        for target in active_phy_targets:
            if "ethernetcopper" in target:
                return target
    if isinstance(active_phy_targets, str) \
            and "ethernetcopper" in target:
        return active_phy_targets

    return ""


def get_stc_ports(stc: stchttp.StcHttp,
                  stc_sessions: List[str]) -> List[StcPort]:
    """
    _summary_

    :param stc: _description_
    :param stc_sessions: _description_
    """
    stc_ports: List[StcPort] = []

    try:
        for session in stc_sessions:
            join_session(stc, session)
            port_handles = list_ports(stc)
            for port_handle in port_handles:
                port_info = get_port_attributes(stc, port_handle)
                if port_info:
                    active_phy_targets = \
                        get_eth_copper_handle_by_port_attr(port_info)
                    if active_phy_targets:
                        eth_copper = get_ethernet_copper_info(
                            active_phy_targets)
                if not port_info and not eth_copper:
                    continue
                port_name = session.replace(STC_SESSION_PREFIX, "")\
                    .replace(STC_SESSION_SUFFIX, "")

                auto_negotiation_role = \
                    eth_copper.get("AutoNegotiationMasterSlave")

                stc_port = StcPort(
                    name=port_name,
                    handle=port_handle,
                    link_status=eth_copper.get("LinkStatus"),
                    auto_negotiation=eth_copper.get("AutoNegotiation"),
                    auto_negotiation_role=auto_negotiation_role,
                    duplex_mode=eth_copper.get("DuplexStatus"),
                    line_speed=eth_copper.get("LineSpeedStatus"))

                stc_ports.append(stc_port)
    except Exception as err:
        msg = "Failed to get STC port information"
        LOG.exception(f"{msg} {err}")
        raise StcPortError(
            message=msg,
            error_details=str(err))

    return stc_ports
