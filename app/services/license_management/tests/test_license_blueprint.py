from mock import MagicMock, PropertyMock, patch

from services.license_management.license_blueprint import _get_licenses

TEST_MODULE = "services.license_management.license_blueprint"


@patch(f"{TEST_MODULE}.LOG")
@patch(f"{TEST_MODULE}.LicenseFile")
def test_get_licenses(file_mock, log_mock):
    # Mock
    mock_lic1 = MagicMock()
    mock_lic1.to_dict.return_value = "ut_lic1"
    mock_lic2 = MagicMock()
    mock_lic2.to_dict.return_value = "ut_lic2"

    mock_licenses = PropertyMock(
        return_value=[mock_lic1, mock_lic2])
    type(file_mock()).licenses = mock_licenses

    # Test return licenses
    ret = _get_licenses()
    assert ret == ["ut_lic1", "ut_lic2"]
    file_mock().read.assert_called_once_with()
    file_mock().parse.assert_called_once_with()
    log_mock.info.assert_not_called()

    # Reset mock
    mock_licenses = PropertyMock(
        return_value=[])
    type(file_mock()).licenses = mock_licenses
    file_mock.reset_mock()
    file_mock().read.side_effect = Exception("ut_error")
    log_mock.reset_mock()

    # Test no licenses found
    ret = _get_licenses()
    assert ret == []
    log_mock.info.assert_called_once_with(
        "No licenses found. ut_error"
    )
