from mock import call, patch

from app import create_app

TEST_MODULE = "app"


@patch(f"{TEST_MODULE}.SECURITY_PASSWORD_SALT")
@patch(f"{TEST_MODULE}.init_datastore")
@patch(f"{TEST_MODULE}.create_admin_role_and_user")
@patch(f"{TEST_MODULE}.generate_routes")
@patch(f"{TEST_MODULE}.JWTManager")
@patch(f"{TEST_MODULE}.Security")
@patch(f"{TEST_MODULE}.Flask")
@patch(f"{TEST_MODULE}.secrets")
@patch(f"{TEST_MODULE}.os")
def test_create_app(os_mock,
                    secrets_mock,
                    flask_mock,
                    security_mock,
                    jwt_mock,
                    routes_mock,
                    user_mock,
                    datastore_mock,
                    salt_mock):
    # Mock
    os_mock.environ.get.side_effect = [
        "ut_key", "ut_salt"
    ]
    secrets_mock.token_urlsafe.side_effect = [
        "ut_sec_key", "ut_jwt_key"
    ]
    datastore_mock.return_value = "ut_datastore"

    ret = create_app()
    flask_mock.assert_called_once_with("app")
    flask_mock().config.__setitem__.assert_has_calls([
        call("SECRET_KEY", "ut_key"),
        call("SECURITY_PASSWORD_SALT", "ut_salt"),
        call("JWT_SECRET_KEY", "ut_jwt_key")
    ])

    os_mock.environ.get.assert_has_calls([
        call("SECRET_KEY", "ut_sec_key"),
        call("SECURITY_PASSWORD_SALT", salt_mock)
    ])
    assert os_mock.environ.get.call_count == 2

    secrets_mock.token_urlsafe.assert_has_calls([
        call(), call()])
    assert secrets_mock.token_urlsafe.call_count == 2

    security_mock.assert_called_once_with(
        ret, "ut_datastore")

    datastore_mock.assert_called_once_with()
    user_mock.assert_called_once_with(ret)
    routes_mock.assert_called_once_with(ret)
    jwt_mock.assert_called_once_with(ret)
