import pytest
from mock import mock_open, patch

from services.license_management.v2x_license import (LicenseFile, V2xLicense,
                                                     _convert_date_format,
                                                     lic_errors)

TEST_MODULE = "services.license_management.v2x_license"


def test_V2xLicense_init():
    v2x_lic = V2xLicense("ut_name", "ut_start", "ut_exp")

    assert v2x_lic.name == "ut_name"
    assert v2x_lic.start == "ut_start"
    assert v2x_lic.expiration == "ut_exp"


def test_V2xLicense_to_dict():
    v2x_lic = V2xLicense("ut_name", "ut_start", "ut_exp")
    assert v2x_lic.to_dict() == {
        "name": "ut_name",
        "start": "ut_start",
        "expiration": "ut_exp"
    }


@patch(f"{TEST_MODULE}.LICENSE_FILE_NAME")
@patch(f"{TEST_MODULE}.LICENSE_PATH")
@patch(f"{TEST_MODULE}.os")
def test_LicenseFile_init(os_mock, path_mock, name_mock):
    # Mock
    os_mock.path.join.return_value = "ut_file_path"

    lic_file = LicenseFile()
    assert lic_file.file_path == "ut_file_path"
    assert lic_file.content is None
    assert lic_file.licenses == []

    os_mock.path.join.assert_called_once_with(
        path_mock,
        name_mock
    )


@patch("builtins.open", new_callable=mock_open, read_data="ut_content")
@patch(f"{TEST_MODULE}.os")
def test_LicenseFile_read_pass(os_mock, mock_open):
    # Test read license file successfully.
    lic_file = LicenseFile()
    lic_file.file_path = "ut_path"

    lic_file.read()
    assert lic_file.content == "ut_content"
    mock_open.assert_called_once_with("ut_path", encoding="utf-8")


@patch("builtins.open",
       side_effect=Exception)
@patch(f"{TEST_MODULE}.os")
def test_LicenseFile_read_fail(os_mock, mock_open):
    # Test raises LicenseFileReadError.
    lic_file = LicenseFile()
    lic_file.file_path = "ut_path"

    with pytest.raises(lic_errors.LicenseFileReadError) as err:
        lic_file.read()
    assert str(err.value) == "Failed to read V2X Virtual license file."


@patch(f"{TEST_MODULE}.os")
def test_LicenseFile_parse_when_content_is_none(os_mock):
    # Test content is None.
    lic_file = LicenseFile()

    lic_file.parse()
    assert lic_file.licenses == []


@patch(f"{TEST_MODULE}.os")
def test_LicenseFile_parse_when_content_is_empty(os_mock):
    # Test content is empty string
    lic_file = LicenseFile()
    lic_file.content = ""

    lic_file.parse()
    assert lic_file.licenses == []


@patch(f"{TEST_MODULE}.os")
def test_LicenseFile_parse_pass(os_mock):
    # Test the content contains the follow licenses:
    # licenses contain the valid name, start, and expiration
    # license contains the valid name, start, expiration, and vendor
    # licenses contain invalid start or expiration
    # licenses do not contain start or expiration
    # license doesn't contain name and vendor
    first_three_lines = \
        "SERVER this_host 525400C53BEE 30225\n" + \
        "VENDOR spirentd port=30226\nUSE_SERVER\n"
    valid_content = \
        "INCREMENT TT3_WSDL_PL spirentd 2024.05 " + \
        "25-may-2024 2 BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-nov-2023 SIGN='0097 A581 C966 9337 20D5 EE0D 3443 \\\n\t" + \
        "9B00 7EF3 80F3 ECCC 121F 322D 76E3 0A80'\n" + \
        "INCREMENT GFE-EP spirentd 2024.05 25-may-2024 2 \\\n\t" + \
        "VENDOR_STRING=NAME=;PN=TEC-DEMO-C50; BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-nov-2023 SIGN='0099 D97F 41E2 BC9E BB45 9592 6593 \\\n\t" + \
        "1100 263B 8BFA 6702 D1CB 798F A205 0A6D'\n"
    conatins_vendor = \
        "INCREMENT AUTO_V2X_APP_CHINA spirentd 1 25-may-2024 2 \\\n\t" + \
        "VENDOR_STRING='NAME=V2X VIRTUAL CHINA APPLICATIONS PACK \\\n\t;" + \
        "PN=TEC-SW-V2X-APP-CHN;ILTYPE=;STYPE=;LICTYPE=;' BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-nov-2023 SIGN='0086 ED22 6C55 04E2 8EAA DB3F 28B0 \\\n\t" + \
        "9700 DEC6 708A CFC4 45D3 2030 58BC BD44'\n"
    invalid_start_or_expiration = \
        "INCREMENT TTsuite-OPEN-IPv6 spirentd " + \
        "2024.05 25-abc-2024 2 BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-nov-2023 SIGN='0069 5B05 DE7D C165 6F5A 18A6 8E66 \\\n\t" + \
        "7C00 4EBE 1666 A187 39FA ADE3 9372 D9A9'\n" + \
        "INCREMENT TTPLUGIN_SUPPORT spirentd 2024.05 25-may-2024 54 \\\n\t" + \
        "VENDOR_STRING=NAME=;PN=TEC-DEMO-C50; BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-abc-2023 SIGN='0064 7BBF 2FD9 DAB0 5853 27F0 EE7B \\\n\t" + \
        "F600 AAFF A660 A387 B798 9152 CAE6 EE4D'\n"
    no_start_or_expiration = \
        "INCREMENT TTsuite-AVB-Exceptions spirentd " + \
        "2024.05 25-may-2024 2 \\\n\t" + \
        "BORROW=336 \\\n\tSN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "SIGN='00BE 17AA 9367 BAD9 1191 56AD BA2E \\\n\t" + \
        "4F00 6301 B5B5 7C5F E181 89C5 5E50 2100'\n" + \
        "INCREMENT TTsuite-AVB-1722 spirentd 2 BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-nov-2023 SIGN='0065 B0FF 6F64 54D7 693C C699 CFE2 \\\n\t" + \
        "1C00 10C7 B153 3F58 38C4 FFFE DAA3 36C8'\n"
    no_name_and_verdor = \
        "INCREMENT  spirentd 2024.05 25-may-2024 2 \\\n\t" + \
        "VENDOR_STRING=NAME=;PN=TEC-DEMO-C50; BORROW=336 \\\n\t" + \
        "SN=02i5c00000Dm1xOAAR:02i5c00000Dm1xOAAR:" + \
        "FID_e8037cc0_91be_405c_9e20_47e686ff4a47 \\\n\t" + \
        "START=27-nov-2023 SIGN='0097 5ED8 51C8 521D 23DE 856E FD20 \\\n\t" + \
        "F600 7382 74DB D646 1089 C75F 990C D5EE'\n"
    mock_content = first_three_lines + valid_content + \
        conatins_vendor + invalid_start_or_expiration + \
        no_start_or_expiration + no_name_and_verdor

    lic_file = LicenseFile()
    lic_file.content = mock_content

    lic_file.parse()
    assert lic_file.licenses[0].to_dict() == {
        "name": "TT3 WSDL PL",
        "start": "2023.11.27",
        "expiration": "2024.05.25"}
    assert lic_file.licenses[1].to_dict() == {
        "name": "GFE EP",
        "start": "2023.11.27",
        "expiration": "2024.05.25"}
    assert lic_file.licenses[2].to_dict() == {
        "name": "AUTO V2X APP CHINA",
        "start": "2023.11.27",
        "expiration": "2024.05.25"}
    assert len(lic_file.licenses) == 3


def test__convert_date_format_pass():
    assert _convert_date_format("25-may-2024") == \
        "2024.05.25"


def test_convert_date_format_fail():
    with pytest.raises(lic_errors.DateFormatError) as err:
        _convert_date_format("ut_input")
    assert str(err.value) == "Invalid date format: ut_input."
