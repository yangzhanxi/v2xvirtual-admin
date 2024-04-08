from mock import MagicMock, call, patch

from services.network_management import net_if_models

TEST_MODULE = "services.network_management.net_if_models"


@patch(f"{TEST_MODULE}.is_valid_ipv4")
def test_Ipv4NetworkInterface_init(ipv4_mock):
    # Mock
    ipv4_mock.return_value = True
    # Test pass
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        name="ut_name",
        address="1.1.1.10",
        gateway="1.1.1.1",
        netmask="24"
    )

    assert ipv4_if.name == "ut_name"
    assert ipv4_if.address == "1.1.1.10"
    assert ipv4_if.gateway == "1.1.1.1"
    assert ipv4_if.netmask == "255.255.255.0"
    ipv4_mock.assert_has_calls([
        call("1.1.1.10"),
        call("1.1.1.1")
    ])
    assert ipv4_mock.call_count == 2

    # Test invalid IPv4 address
    ipv4_mock.reset_mock()
    ipv4_mock.side_effect = [False, True]
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        name="ut_name",
        address="a.b.c.d",
        gateway="1.1.1.1",
        netmask="24"
    )
    try:
        ipv4_if.address
    except net_if_models.if_errors.InvalidIpv4AddressError as err:
        assert str(err) == "a.b.c.d is invalid IPv4 Address."

    # Test invalid Gateway
    ipv4_mock.reset_mock()
    ipv4_mock.side_effect = [True, False]
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        name="ut_name",
        address="1.1.1.10",
        gateway="a.b.c.d",
        netmask="24"
    )
    try:
        ipv4_if.gateway
    except net_if_models.if_errors.InvalidIpv4AddressError as err:
        assert str(err) == "a.b.c.d is invalid IPv4 Address."

    # Test invalid netmask (netmask < 0)
    ipv4_mock.reset_mock()
    ipv4_mock.side_effect = None
    ipv4_mock.return_value = True
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        name="ut_name",
        address="1.1.1.10",
        gateway="1.1.1.1",
        netmask="-1"
    )
    try:
        ipv4_if.netmask
    except net_if_models.if_errors.GettingNetworkInterfaceError as err:
        assert str(err) == "-1 is invalid netmask."

    # Test invalid netmask (netmask > 33)
    ipv4_mock.reset_mock()
    ipv4_mock.return_value = True
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        name="ut_name",
        address="1.1.1.10",
        gateway="1.1.1.1",
        netmask="34"
    )
    try:
        ipv4_if.netmask
    except net_if_models.if_errors.GettingNetworkInterfaceError as err:
        assert str(err) == "34 is invalid netmask."


@patch(f"{TEST_MODULE}.subprocess")
def test_list_network_info(subprocess_mock):
    # Test pass
    ret_mock = MagicMock()
    ret_mock.stdout = "ut_ret".encode("utf-8")
    ret_mock.stderr = None
    subprocess_mock.run.return_value = ret_mock

    assert net_if_models.list_network_info() == "ut_ret"

    # Test raise exception
    ret_mock = MagicMock()
    ret_mock.stdout = "ut_ret".encode("utf-8")
    ret_mock.stderr = "ut_error".encode("utf-8")
    subprocess_mock.run.return_value = ret_mock

    try:
        net_if_models.list_network_info()
    except net_if_models.if_errors.GettingNetworkInterfaceError as err:
        assert str(err) == "ut_error"


@patch(f"{TEST_MODULE}.get_stc_network_interface")
def test_get_stc_network_interfaces(net_if_mock):
    # Mock
    net_if_mock.side_effect = ["ut_if1", "ut_if2"]
    net_info_mock = "1: ut_net1\n ut_addr1\n2: ut_net2\n ut_addr2"
    assert net_if_models.get_stc_network_interfaces(net_info_mock) == \
        ["ut_if1", "ut_if2"]
    net_if_mock.assert_has_calls([
        call("1: ut_net1 ut_addr1"),
        call("2: ut_net2 ut_addr2")])
    assert net_if_mock.call_count == 2


@patch(f"{TEST_MODULE}.Ipv4NetworkInterface")
def test_get_stc_network_interface(ipv4_if_mock):
    # Test returns IPv4 network interface object.
    net_if_mock = "2: slot1port2: inet 1.1.1.2/24"
    ret = net_if_models.get_stc_network_interface(net_if_mock)
    ipv4_if_mock.assert_called_once_with(
        "slot1port2", "1.1.1.2", "", "24")
    assert ret == ipv4_if_mock()

    # Test returns None when slotport doesn't match
    assert net_if_models.get_stc_network_interface(
        "2: eth0: inet 1.1.1.2/24") is None

    # Test returns None when ipv4 address doesn't match
    assert net_if_models.get_stc_network_interface(
        "2: slot1port2: inet a.b.c.d/24") is None


def test_list_ifs_by_part_num():
    # Test returns net if when part num is SPT-M1
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        "slot7port2", "1.1.2.3", "", "18"
    )
    assert net_if_models.list_ifs_by_part_num(
        "SPT-M1", [ipv4_if]) == [ipv4_if]

    # Test returns net if when part num is SPT-C50
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        "slot1port3", "1.1.2.3", "", "18"
    )
    assert net_if_models.list_ifs_by_part_num(
        "SPT-C50", [ipv4_if]) == [ipv4_if]

    # Test returns an empty list
    ipv4_if = net_if_models.Ipv4NetworkInterface(
        "slot1port3", "1.1.2.3", "", "18"
    )
    assert net_if_models.list_ifs_by_part_num(
        "SPT-M1", [ipv4_if]) == []


@patch(f"{TEST_MODULE}.LOG.debug")
@patch(f"{TEST_MODULE}.list_ifs_by_part_num")
@patch(f"{TEST_MODULE}.get_stc_network_interfaces")
@patch(f"{TEST_MODULE}.list_network_info")
def test_get_network_interface(list_mock,
                               stc_if_mock,
                               list_ifs_mock,
                               debug_mock):
    list_mock.return_value = "ut_network_info"
    stc_if_mock.return_value = "ut_stc_if"
    list_ifs_mock.return_value = "ut_ifs"

    assert net_if_models.get_network_interfaces(
        "ut_pn") == "ut_ifs"
    debug_mock.assert_has_calls([
        call("Network interfaces:\nut_network_info"),
        call("STC network interfaces:\nut_stc_if"),
        call("STC test port interfaces:\nut_ifs")
    ])
    list_mock.assert_called_once_with()
    stc_if_mock.assert_called_once_with(
        "ut_network_info"
    )
    list_ifs_mock.assert_called_once_with(
        "ut_pn", "ut_stc_if")

    # Test raises Exception
    list_mock.side_effect = Exception("ut_error")

    try:
        net_if_models.get_network_interfaces("ut_pn")
    except net_if_models.if_errors.NetworkInfoError as err:
        assert str(err) == "Failed to get network interface information."
        assert str(err.error_info) == "ut_error"
