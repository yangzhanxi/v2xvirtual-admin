import logging
from typing import Dict, List

from stcrestclient import stchttp

from const import APP_LOGGER, STC_SESSION_PREFIX, STC_SESSION_SUFFIX
from errors.stc_errors import StcPortError
from services.network_management.stc_port_models import StcPort

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


def get_port_attributes(stc: stchttp.StcHttp,
                        port_handle: str) -> Dict[str, str]:
    """
    _summary_

    :param stc: _description_
    :param port_handle: _description_
    """
    return stc.get(port_handle)


def get_phy_info(stc: stchttp.StcHttp,
                 phy_handle: str) -> Dict[str, str]:
    """
    _summary_

    :param stc: _description_
    :param phy_info: _description_
    """
    phy_info = stc.get(phy_handle)

    return phy_info


def get_active_phy(port_info: dict) -> str:
    """
    _summary_

    :param port_info: _description_
    """
    active_phys = port_info.get("activephy-Targets")
    supported_phys = port_info.get("SupportedPhys")
    if supported_phys:
        phys = [phy.replace("_", "").lower()
                for phy in supported_phys.split("|")]

        if isinstance(active_phys, list):
            for target in active_phys:
                for phy in phys:
                    if phy in target:
                        return target

        if isinstance(active_phys, str):
            for phy in phys:
                if phy in active_phys:
                    return active_phys

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
                    active_phy = \
                        get_active_phy(port_info)
                    if active_phy:
                        phy_info = get_phy_info(stc, active_phy)
                if not port_info and not phy_info:
                    continue
                port_name = session.replace(STC_SESSION_PREFIX, "")\
                    .replace(STC_SESSION_SUFFIX, "")

                auto_negotiation_role = \
                    phy_info.get("AutoNegotiationMasterSlave", "")

                stc_port = StcPort(
                    name=port_name,
                    handle=port_handle,
                    link_status=phy_info.get("LinkStatus", ""),
                    auto_negotiation=phy_info.get("AutoNegotiation", ""),
                    auto_negotiation_role=auto_negotiation_role,
                    duplex_mode=phy_info.get("DuplexStatus", ""),
                    line_speed=phy_info.get("LineSpeedStatus", ""))

                stc_ports.append(stc_port)

    except Exception as err:
        msg = "Failed to get STC port information"
        LOG.exception(f"{msg} {err}")
        raise StcPortError(
            message=msg,
            error_details=str(err))

    return stc_ports
