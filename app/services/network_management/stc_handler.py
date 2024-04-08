import logging
from typing import Dict, List

from stcrestclient import stchttp

from const import APP_LOGGER, STC_SESSION_PREFIX, STC_SESSION_SUFFIX
from errors import stc_errors
from services.network_management.stc_port_models import StcPort

LOG = logging.getLogger(APP_LOGGER)


def list_sessions(stc: stchttp.StcHttp) -> List[str]:
    """
    List STC sessions.

    :param stc: STC rest client instance.
    :raises stc_errors.StcSessionError: Failed to get STC session(s).
    :return: A list of STC sessions.
    """
    try:
        stc_sessions = stc.sessions()
        LOG.debug(f"STC sessions: {stc_sessions}")
    except Exception as err:
        msg = "Failed to get STC session(s)."
        LOG.exception(f"{msg} {err}")
        raise stc_errors.StcSessionError(
            message=msg,
            error_details=str(err))

    return stc_sessions


def join_session(stc: stchttp.StcHttp, session_name: str) -> None:
    """
    _summary_

    :param stc: STC rest client instance.
    :param session_name: The name of STC session.
    """
    try:
        stc.join_session(session_name)
        LOG.debug(f"Joined session {session_name}")
    except Exception as err:
        msg = f"Failed to join session {session_name}."
        LOG.exception(f"{msg} {err}")
        raise stc_errors.StcSessionError(
            message=msg,
            error_details=str(err))


def list_ports(stc: stchttp.StcHttp) -> List[str]:
    """
    List STC ports.

    :param stc: STC rest client instance.
    :return: A list of STC port handles.
    """
    try:
        ret = stc.get("project1", "children-port")
        LOG.debug(f"STC ports: {ret}")

        if isinstance(ret, str):
            return [ret]
    except Exception as err:
        msg = "Failed to list STC ports."
        LOG.exception(f"{msg} {err}")
        raise stc_errors.StcPortError(
            message=msg,
            error_details=str(err))

    return ret


def get_port_attributes(stc: stchttp.StcHttp,
                        port_handle: str) -> Dict[str, str]:
    """
    Gets attributes for specifiec STC port.

    :param stc: STC rest client instance.
    :param port_handle: STC port handle.
    :return: Dictionary contains STC port attributes.
    """
    try:
        ret = stc.get(port_handle)
        LOG.debug(f"Port handle: {port_handle}\n{ret}")
    except Exception as err:
        msg = "Failed to get port {port_handle}."
        LOG.exception(f"{msg} {err}")
        raise stc_errors.StcPortError(
            message=msg,
            error_details=str(err))
    return ret


def get_phy_info(stc: stchttp.StcHttp,
                 phy_handle: str) -> Dict[str, str]:
    """
    Gets phy info by phy handle.

    :param stc: STC rest client instance.
    :param phy_info: STC phy information.
    :return: Dictionary contains STC phy attributes.
    """
    try:
        phy_info = stc.get(phy_handle)
        LOG.debug(f"Phy handle: {phy_handle}\n{phy_info}")
    except Exception as err:
        msg = "Failed to get active phy: {phy_handle}."
        LOG.exception(f"{msg} {err}")
        raise stc_errors.StcPhyError(
            message=msg,
            error_details=str(err))

    return phy_info


def get_active_phy(port_info: dict) -> str:
    """
    Gets active phy for the specified port.

    :param port_info: Dictionary contanis STC port attributs.
    :return: STC phy handle.
    """
    active_phy = port_info.get("activephy-Targets", "")
    supported_phys = port_info.get("SupportedPhys", "")
    if supported_phys:
        phys = [phy.replace("_", "").lower()
                for phy in supported_phys.split("|")]

        if isinstance(active_phy, list):
            for target in active_phy:
                for phy in phys:
                    if phy in target:
                        LOG.debug("Active phy: {target}")
                        return target

        if isinstance(active_phy, str):
            for phy in phys:
                if phy in active_phy:
                    LOG.debug("Active phy: {active_phys}")
                    return active_phy

    return ""


def get_stc_ports(stc: stchttp.StcHttp,
                  stc_sessions: List[str]) -> List[StcPort]:
    """
    Gets STC ports.

    :param stc: STC rest client instance.
    :param stc_sessions: A list of STC session names.
    :return: A list of StcPort objects.
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
                if not port_info or not phy_info:
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
        msg = "Failed to get STC ports."
        LOG.exception(f"{msg} {err}")

    return stc_ports
