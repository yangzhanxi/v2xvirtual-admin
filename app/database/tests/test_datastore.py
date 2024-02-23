from mock import MagicMock, patch

from database.datastore import (AdminRoleCreateError, AdminUserCreateError,
                                DatastoreInitError, create_admin_role,
                                create_admin_role_and_user, create_admin_user,
                                init_datastore)

TEST_MODULE = "database.datastore"


@patch(f"{TEST_MODULE}.app_const")
@patch(f"{TEST_MODULE}.User")
@patch(f"{TEST_MODULE}.Role")
@patch(f"{TEST_MODULE}.MongoEngineUserDatastore")
@patch(f"{TEST_MODULE}.connect")
def test_init_datastore(connect_mock,
                        mongo_mock,
                        role_mock,
                        user_mock,
                        const_mock):
    # Mock
    connect_mock.return_value = "ut_db"
    # Test pass
    ret = init_datastore()

    mongo_mock.assert_called_once_with(
        "ut_db", user_mock, role_mock
    )
    assert ret == mongo_mock()
    connect_mock.assert_called_once_with(
        alias=const_mock.DB_NAME,
        db=const_mock.DB_NAME,
        username=const_mock.ROOT,
        password=const_mock.ROOT_PASSWORD,
        host=const_mock.DB_HOST,
        port=const_mock.DB_PORT)

    # Test raises DatastoreInitError exception
    connect_mock.reset_mock()
    connect_mock.side_effect = DatastoreInitError("ut_error")
    mongo_mock.reset_mock()
    role_mock.reset_mock()
    user_mock.reset_mock()
    const_mock.reset_mock()

    try:
        init_datastore()
    except DatastoreInitError as err:
        assert str(err) == "Failed to connect MongoDB."
        assert str(err.error_info) == "ut_error"


def test_create_admin_role():
    # Mock
    mock_datastore = MagicMock()
    # Test pass
    create_admin_role(mock_datastore)
    mock_datastore.find_or_create_role.assert_called_once_with(
        name="admin", permissions=["admin-write", "admin-read"])

    # Test raises AdminRoleCreateError
    mock_datastore.reset_mock()
    mock_datastore.find_or_create_role.side_effect = Exception("ut_error")

    try:
        create_admin_role(mock_datastore)
    except AdminRoleCreateError as err:
        assert str(err) == "Failed to create Admin role."
        assert err.error_info == "ut_error"


@patch(f"{TEST_MODULE}.hash_password")
def test_create_admin_user(hash_mock):
    # Mock
    mock_datastore = MagicMock()
    mock_datastore.find_user.return_value = False
    hash_mock.return_value = "ut_hash"
    # Test pass with create user
    create_admin_user(mock_datastore)
    mock_datastore.find_user.assert_called_once_with(
        username="admin")
    mock_datastore.create_user.assert_called_once_with(
        username="admin",
        password="ut_hash",
        roles=["admin"])
    hash_mock.assert_called_once_with("password")

    # Test passes when user exists
    mock_datastore.reset_mock()
    mock_datastore.find_user.return_value = True
    hash_mock.reset_mock()

    create_admin_user(mock_datastore)
    mock_datastore.find_user.assert_called_once_with(
        username="admin")
    mock_datastore.create_user.assert_not_called()
    hash_mock.assert_not_called()

    # Test raises AdminUserCreateError exception
    mock_datastore.reset_mock()
    mock_datastore.side_effect == Exception("ut_error")
    hash_mock.reset_mock()
    try:
        create_admin_user(mock_datastore)
    except AdminUserCreateError as err:
        assert str(err) == "Failed to create Admin user."
        assert err.error_info == "ut_error"


# @patch("builtins.getattr")
@patch(f"{TEST_MODULE}.create_admin_user")
@patch(f"{TEST_MODULE}.create_admin_role")
def test_create_admin_role_and_user(role_mock, user_mock):
    # Mock
    app_mock = MagicMock()
    app_mock.security.datastore.return_value = "ut_store"
    # sec_mock = MagicMock()
    # datastore_mock = MagicMock()
    # app_mock.security = sec_mock()
    # get_mock.retun_value = "ut_store"

    create_admin_role_and_user(app_mock)
    app_mock.app_context.assert_called_once_with()
    role_mock.assert_called_once_with(app_mock.security.datastore)
    user_mock.assert_called_once_with(app_mock.security.datastore)
