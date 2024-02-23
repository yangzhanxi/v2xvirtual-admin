from mock import MagicMock, call, patch

from routes import generate_routes

TEST_MODULE = "routes"


@patch(f"{TEST_MODULE}.lic_bp")
@patch(f"{TEST_MODULE}.auth_bp")
def test_generate_routes(auth_mock, lic_mock):
    # Mock
    app_mock = MagicMock()

    generate_routes(app_mock)
    app_mock.register_blueprint.assert_has_calls([
        call(auth_mock, url_prefix="/api"),
        call(lic_mock, url_prefix="/api")
    ])
