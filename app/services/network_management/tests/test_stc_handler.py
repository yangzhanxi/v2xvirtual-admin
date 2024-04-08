from mock import MagicMock, call, patch

import services.network_management.stc_handler as tc_module

TC_MODULE = "services.network_management.stc_handler"


@patch(f"{TC_MODULE}.LOG")
def test_list_sessions(log_mock):
    # Test returns sessions
    stc_mock = MagicMock()
    stc_mock.sessions.return_value = ["ut_s1", "ut_s2"]

    ret = tc_module.list_sessions(stc_mock)
    stc_mock.sessions.assert_called_once_with()
    assert ret == ["ut_s1", "ut_s2"]
    log_mock.debug("STC sessions: [ut_s1, ut_s2]")

    # Test raises Failed to get STC sessions exception
    stc_mock.sessions.side_effect = Exception("ut_error")
    try:
        tc_module.list_sessions(stc_mock)
    except tc_module.stc_errors.StcSessionError as err:
        assert str(err) == "Failed to get STC session(s)."
        assert str(err.error_info) == "ut_error"
        log_mock.exception.assert_called_once_with(
            "Failed to get STC session(s). ut_error")


@patch(f"{TC_MODULE}.LOG")
def test_join_session(log_mock):
    # Test pass
    stc_mock = MagicMock()
    tc_module.join_session(stc_mock, "ut_sess")
    log_mock.debug.assert_called_once_with(
        "Joined session ut_sess")
    stc_mock.join_session.assert_called_with("ut_sess")

    # Test raises Failed to join session exception
    stc_mock.reset_mock()
    stc_mock.side_effect = Exception("ut_error")

    try:
        tc_module.join_session(stc_mock, "ut_sess")
    except tc_module.stc_errors.StcSessionError as err:
        assert str(err) == "Failed to join session ut_sess"
        assert str(err.error_info) == "ut_error"
        log_mock.exception.assert_called_once_with(
            "Failed to join STC session ut_sess ut_error")


@patch(f"{TC_MODULE}.LOG")
def test_list_ports(log_mock):
    # Mock
    stc_mock = MagicMock()
    stc_mock.get.return_value = "ut_port"

    # Test pass
    assert tc_module.list_ports(stc_mock) == ["ut_port"]
    stc_mock.get.assert_called_once_with(
        "project1", "children-port")
    log_mock.debug.assert_called_once_with(
        "STC ports: ut_port")

    # Test raises Exception
    stc_mock.get.side_effect = Exception("ut_error")

    try:
        tc_module.list_ports(stc_mock)
    except tc_module.stc_errors.StcPortError as err:
        assert str(err) == "Failed to list STC ports."
        assert err.error_info == "ut_error"
        assert log_mock.exception(
            "Failed to list STC ports ut_error")


@patch(f"{TC_MODULE}.LOG")
def test_get_port_attributes(log_mock):
    # Mock
    stc_mock = MagicMock()
    stc_mock.get.return_value = "ut_attr"

    # Test pass
    assert tc_module.get_port_attributes(
        stc_mock, "ut_port") == "ut_attr"
    stc_mock.get.assert_called_once_with(
        "ut_port")
    log_mock.debug(
        "Port Handle: ut_port\nut_attr")

    # Test raises Failed to get port exception
    stc_mock.side_effect = Exception("ut_error")
    try:
        tc_module.get_port_attributes(stc_mock, "ut_port")
    except tc_module.stc_errors.StcPortError as err:
        assert str(err) == "Failed to get port ut_port."
        assert err.error_info == "ut_error"
        log_mock.exception.assert_called_once_with(
            "Failed to get port ut_port. ut_error")


@patch(f"{TC_MODULE}.LOG")
def test_get_phy_info(log_mock):
    # Mock
    stc_mock = MagicMock()
    stc_mock.get.return_value = "ut_attr"

    # Test pass
    assert tc_module.get_phy_info(
        stc_mock, "ut_handle") == "ut_attr"
    log_mock.debug.assert_called_once_with(
        "Phy handle: ut_handle\nut_attr")

    # Test raises Failed to get active phy exception
    stc_mock.side_effect = Exception("ut_error")
    try:
        tc_module.get_phy_info(stc_mock, "ut_handle")
    except tc_module.stc_errors.StcPhyError as err:
        assert str(err) == \
            "Failed to get active phy: ut_handle."
        assert err.error_info == "ut_error"
        assert log_mock.exception.assert_called_once_with(
            "Failed to get active phy: ut_handle. ut_error")


def test_get_active_phy():
    # Mock
    port_mock = {
        "activephy-Targets": "ethernetcopper1",
        "SupportedPhys": "ETHERNET_COPPER|ETHERNET_FIBBER"
    }

    # Test pass when activephy targets is string
    assert tc_module.get_active_phy(port_mock) == "ethernetcopper1"

    # Test pass when activephy target is a list
    port_mock = {
        "activephy-Targets": ["ut_phy1", "ethernetfiber1"],
        "SupportedPhys": "ETHERNET_COPPER|ETHERNET_FIBER"
    }
    assert tc_module.get_active_phy(port_mock) == "ethernetfiber1"

    # Test returns empty string
    port_mock = {
        "activephy-Targets": ["ut_phy1"],
        "SupportedPhys": "ETHERNET_COPPER|ETHERNET_FIBER"
    }
    assert tc_module.get_active_phy(port_mock) == ""


@patch(f"{TC_MODULE}.LOG")
@patch(f"{TC_MODULE}.get_phy_info")
@patch(f"{TC_MODULE}.get_active_phy")
@patch(f"{TC_MODULE}.get_port_attributes")
@patch(f"{TC_MODULE}.list_ports")
@patch(f"{TC_MODULE}.join_session")
def test_get_stc_ports(sess_mock,
                       ports_mock,
                       attrs_mock,
                       phy_mock,
                       phy_info_mock,
                       log_mock):
    # Mock
    stc_mock = MagicMock()
    ports_mock.side_effect = [["ut_port1"], ["ut_port2"]]
    port_infos = [
        {
            "activephy-Targets": "ethernetcopper1",
            "SupportedPhys": "ETHERNET_COPPER|ETHERNET_FIBBER"
        },
        {
            "activephy-Targets": ["ut_phy1", "ethernetfiber1"],
            "SupportedPhys": "ETHERNET_COPPER|ETHERNET_FIBER"
        }
    ]
    attrs_mock.side_effect = port_infos
    phy_mock.side_effect = ["ut_phy_handle1", "ut_phy_handle2"]
    phy_infos = [
        {
            "LinkStatus": "ut_status1",
            "AutoNegotiation": "true",
            "AutoNegotiationMasterSlave": "ut_role1",
            "DuplexStatus": "ut_full1",
            "LineSpeedStatus": "ut_speed1",
        }, {
            "LinkStatus": "ut_status2",
            "AutoNegotiation": "true",
            "AutoNegotiationMasterSlave": "ut_role2",
            "DuplexStatus": "ut_full2",
            "LineSpeedStatus": "ut_speed2",
        }
    ]
    phy_info_mock.side_effect = phy_infos
    sessions = [
        "TTwb_slot7port1 - ttwb",
        "TTwb_slot7port2 - ttwb"]

    # Test pass
    ret = tc_module.get_stc_ports(stc_mock, sessions)
    assert ret[0].name == "slot7port1"
    assert ret[0].handle == "ut_port1"
    assert ret[0].auto_negotiation == "true"
    assert ret[0].auto_negotiation_role == "ut_role1"
    assert ret[0].duplex_mode == "ut_full1"
    assert ret[0].line_speed == "ut_speed1"
    assert ret[0].link_status == "ut_status1"

    assert ret[1].name == "slot7port2"
    assert ret[1].handle == "ut_port2"
    assert ret[1].auto_negotiation == "true"
    assert ret[1].auto_negotiation_role == "ut_role2"
    assert ret[1].duplex_mode == "ut_full2"
    assert ret[1].line_speed == "ut_speed2"
    assert ret[1].link_status == "ut_status2"

    sess_mock.assert_has_calls([
        call(stc_mock, sessions[0]),
        call(stc_mock, sessions[1])
    ])
    assert sess_mock.call_count == 2
    ports_mock.assert_has_calls([
        call(stc_mock),
        call(stc_mock)
    ])
    assert ports_mock.call_count == 2
    attrs_mock.assert_has_calls([
        call(stc_mock, "ut_port1"),
        call(stc_mock, "ut_port2")
    ])
    assert attrs_mock.call_count == 2
    phy_mock.assert_has_calls([
        call(port_infos[0]),
        call(port_infos[1])
    ])
    assert phy_mock.call_count == 2
    phy_info_mock.assert_has_calls([
        call(stc_mock, "ut_phy_handle1"),
        call(stc_mock, "ut_phy_handle2")
    ])
    assert phy_info_mock.call_count == 2

    # Test returns empty list
    attrs_mock.reset_mock()
    attrs_mock.side_effect = None
    attrs_mock.return_value = ""
    ports_mock.reset_mock()
    ports_mock.side_effect = [["ut_port1"], ["ut_port2"]]

    assert tc_module.get_stc_ports(stc_mock, sessions) == []

    # Test log exception
    sess_mock.reset_mock()
    sess_mock.side_effect = tc_module.stc_errors.StcSessionError(
        message="Failed to join STC session.",
        error_details="ut_error"
    )

    assert tc_module.get_stc_ports(stc_mock, sessions) == []
    log_mock.exception.assert_called_once_with(
        "Failed to get STC ports. Failed to join STC session."
    )
