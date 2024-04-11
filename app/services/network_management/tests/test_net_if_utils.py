from services.network_management.net_if_models import (is_valid_ipv4,
                                                       netmask_to_ipv4_addr)


def test_is_valid_ipv4():
    # Test pass
    assert is_valid_ipv4("1.0.0.0") is True
    assert is_valid_ipv4("1.1.1.1") is True
    assert is_valid_ipv4("255.0.0.0") is True
    assert is_valid_ipv4("255.255.255.255") is True

    # Test returns false
    assert is_valid_ipv4("1.1") is False
    assert is_valid_ipv4("1.1.1.1.11") is False
    assert is_valid_ipv4("1.2.3.b") is False
    assert is_valid_ipv4("1.2.4.268") is False


def test_netmask_to_ipv4_addr():
    assert netmask_to_ipv4_addr(0) == "0.0.0.0"
    assert netmask_to_ipv4_addr(1) == "128.0.0.0"
    assert netmask_to_ipv4_addr(8) == "255.0.0.0"
    assert netmask_to_ipv4_addr(16) == "255.255.0.0"
    assert netmask_to_ipv4_addr(18) == "255.255.192.0"
    assert netmask_to_ipv4_addr(22) == "255.255.252.0"
    assert netmask_to_ipv4_addr(24) == "255.255.255.0"
    assert netmask_to_ipv4_addr(28) == "255.255.255.240"
    assert netmask_to_ipv4_addr(32) == "255.255.255.255"
