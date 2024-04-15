from mock import MagicMock, PropertyMock, patch

from errors.stc_errors import StcSessionError
from services.network_management import network_mgmt_handler as tc_module

TC_MODULE = "services.network_management.network_mgmt_handler"


def test_get_part_num_by_session():
    # Test returns SPT-M1
    assert tc_module.get_part_num_by_session(
         "TTwb_slot7port1 - ttwb") == "SPT-M1"

    # Test returns SPT-C50
    assert tc_module.get_part_num_by_session(
         "TTwb_slot1port4 - ttwb") == "SPT-C50"


def test_build_ports_response():
    # Mock
    port1_mock = MagicMock()
    type(port1_mock).name = PropertyMock(return_value="ut_s1p1")
    type(port1_mock).handle = PropertyMock(return_value="ut_handle1")
    type(port1_mock).link_status = PropertyMock(return_value="ut_status1")
    type(port1_mock).auto_negotiation = PropertyMock(return_value="ut_auto1")
    type(port1_mock).auto_negotiation_role = \
        PropertyMock(return_value="ut_role1")
    type(port1_mock).duplex_mode = PropertyMock(return_value="ut_mode1")
    type(port1_mock).line_speed = PropertyMock(return_value="ut_speed1")

    port2_mock = MagicMock()
    type(port2_mock).name = PropertyMock(return_value="ut_s1p2")
    type(port2_mock).handle = PropertyMock(return_value="ut_handle2")
    type(port2_mock).link_status = PropertyMock(return_value="ut_status2")
    type(port2_mock).auto_negotiation = PropertyMock(return_value="ut_auto2")
    type(port2_mock).auto_negotiation_role = \
        PropertyMock(return_value="ut_role2")
    type(port2_mock).duplex_mode = PropertyMock(return_value="ut_mode2")
    type(port2_mock).line_speed = PropertyMock(return_value="ut_speed2")

    if1_mock = MagicMock()
    type(if1_mock).name = PropertyMock(return_value="ut_s1p1")
    type(if1_mock).address = PropertyMock(return_value="ut_addr1")
    type(if1_mock).gateway = PropertyMock(return_value="ut_g1")
    type(if1_mock).netmask = PropertyMock(return_value="ut_netmask1")

    if2_mock = MagicMock()
    type(if2_mock).name = PropertyMock(return_value="ut_s1p2")
    type(if2_mock).address = PropertyMock(return_value="ut_addr2")
    type(if2_mock).gateway = PropertyMock(return_value="ut_g2")
    type(if2_mock).netmask = PropertyMock(return_value="ut_netmask2")

    if3_mock = MagicMock()
    type(if3_mock).name = PropertyMock(return_value="ut_s1p3")
    type(if3_mock).address = PropertyMock(return_value="ut_addr3")
    type(if3_mock).gateway = PropertyMock(return_value="ut_g3")
    type(if3_mock).netmask = PropertyMock(return_value="ut_netmask3")

    ret = tc_module.build_ports_response(
        [if1_mock, if2_mock, if3_mock],
        [port1_mock, port2_mock]
    )

    assert ret == [
        {
            "port_name": {
                "label": "Port Name", "value": "ut_s1p1"},
            "port_handel": {
                "label": "Port Handel", "value": "ut_handle1"},
            "line_speed": {
                "label": "Line Speed", "value": "ut_speed1"},
            "link_status": {
                "label": "Link Status", "value": "ut_status1"},
            "auto_negotiation": {
                "label": "Auto-Negotiation", "value": "ut_auto1"},
            "auto_negotiation_role": {
                "label": "Auto-Negotiation Role", "value": "ut_role1"},
            "duplex_mode": {
                "label": "Duplex Mode", "value": "ut_mode1"},
            "ip_version": {
                "label": "IP version", "value": "IPv4"},
            "address": {
                "label": "IP Address", "value": "ut_addr1"},
            "netmask": {
                "label": "Netmask", "value": "ut_netmask1"},
            "gateway": {
                "label": "Gateway", "value": "ut_g1"}
        },
        {
            "port_name": {
                "label": "Port Name", "value": "ut_s1p2"},
            "port_handel": {
                "label": "Port Handel", "value": "ut_handle2"},
            "line_speed": {
                "label": "Line Speed", "value": "ut_speed2"},
            "link_status": {
                "label": "Link Status", "value": "ut_status2"},
            "auto_negotiation": {
                "label": "Auto-Negotiation", "value": "ut_auto2"},
            "auto_negotiation_role": {
                "label": "Auto-Negotiation Role", "value": "ut_role2"},
            "duplex_mode": {
                "label": "Duplex Mode", "value": "ut_mode2"},
            "ip_version": {
                "label": "IP version", "value": "IPv4"},
            "address": {
                "label": "IP Address", "value": "ut_addr2"},
            "netmask": {
                "label": "Netmask", "value": "ut_netmask2"},
            "gateway": {
                "label": "Gateway", "value": "ut_g2"}
        }
    ]


@patch(f"{TC_MODULE}.LOG")
@patch(f"{TC_MODULE}.build_ports_response")
@patch(f"{TC_MODULE}.net_if_models")
@patch(f"{TC_MODULE}.stc_handler")
@patch(f"{TC_MODULE}.stchttp")
def test_ports_handler(http_mock,
                       stc_mock,
                       if_mock,
                       response_mock,
                       log_mock):
    # Mock
    http_mock.StcHttp.return_value = "ut_stc"
    sessions = ["ut_sess1", "ut_sess2"]
    stc_mock.list_sessions.return_value = sessions
    ports = ["ut_p1", "ut_p2"]
    stc_mock.get_stc_ports.return_value = ports
    stc_mock.get_part_num.return_value = "ut_pn"
    ifs = ["ut_if1", "ut_if2"]
    if_mock.get_network_interfaces.return_value = ifs
    response_mock.return_value = "ut_ports"

    assert tc_module.ports_handler() == "ut_ports"
    http_mock.StcHttp.assert_called_once_with(
        "127.0.0.1", port=8888)
    stc_mock.list_sessions.assert_called_once_with(
        "ut_stc")
    stc_mock.get_stc_ports.assert_called_once_with(
        "ut_stc", sessions)
    stc_mock.get_part_num.assert_called_once_with(
        "ut_stc")
    if_mock.get_network_interfaces.assert_called_once_with(
        "ut_pn")
    response_mock.assert_called_once_with(
        ifs, ports)
    log_mock.assert_not_called()

    # Test resturns empty list
    stc_mock.list_sessions.return_value = []
    assert tc_module.ports_handler() == []

    # Test log exception
    stc_mock.list_sessions.side_effect = \
        StcSessionError("ut_msg", error_details="ut_error")

    assert tc_module.ports_handler() == []
    log_mock.exception.assert_called_once_with(
        "ut_msg ut_error")


@patch(f"{TC_MODULE}.LOG")
@patch(f"{TC_MODULE}.stc_handler")
@patch(f"{TC_MODULE}.stchttp")
def test_part_num_handler(http_mock,
                          stc_mock,
                          log_mock):
    # Test returns part num
    http_mock.StcHttp.return_value = "ut_stc"
    sessions = ["ut_sess1", "ut_sess2"]
    stc_mock.list_sessions.return_value = sessions
    stc_mock.get_part_num.return_value = "ut_pn"

    assert tc_module.part_num_handler() == {
        "part_num": "ut_pn"}
    http_mock.StcHttp.assert_called_once_with(
        "127.0.0.1", port=8888)
    stc_mock.list_sessions.assert_called_once_with(
        "ut_stc")
    stc_mock.join_session.assert_called_once_with(
        "ut_stc", "ut_sess1")
    stc_mock.get_part_num.assert_called_once_with(
        "ut_stc")

    # Test returns no part num.
    stc_mock.list_sessions.return_value = []
    assert tc_module.part_num_handler() == {
        "part_num": ""}

    # Test log exception
    stc_mock.list_sessions.side_effect = \
        StcSessionError("ut_msg", error_details="ut_error")
    assert tc_module.ports_handler() == []
    log_mock.exception.assert_called_once_with(
        "ut_msg ut_error")
