from services.network_management.stc_port_models import StcPort


def test_stcport_init():
    port = StcPort(name="ut_name",
                   handle="ut_handle",
                   link_status="ut_status",
                   auto_negotiation="ut_true",
                   auto_negotiation_role="ut_role",
                   duplex_mode="ut_mode",
                   line_speed="ut_speed")

    assert port.name == "ut_name"
    assert port.handle == "ut_handle"
    assert port.link_status == "ut_status"
    assert port.auto_negotiation == "ut_true"
    assert port.auto_negotiation_role == "ut_role"
    assert port.duplex_mode == "ut_mode"
    assert port.line_speed == "ut_speed"
