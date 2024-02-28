from mock import PropertyMock, call, patch

from errors.app_errors import LoggingConfigurationError
from logging_module import config_log, create_log_config_dict

TEST_MODULE = "logging_module"


@patch(f"{TEST_MODULE}.logging")
def test_create_log_config_dict(logging_mock):
    # mock
    level_mock = PropertyMock(return_value="ut_debug")
    type(logging_mock).DEBUG = level_mock

    # Test create config dict when log level is not DEBUG.
    ret = create_log_config_dict("ut_path", "ut_info")
    assert ret == {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - [%(levelname)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "ut_path",
                "formatter": "standard",
                "maxBytes": 1000000,
                "backupCount": 3,
                "encoding": "utf-8",
            }
        },
        "loggers": {
            "app_logger": {
                "handlers": ["file_handler"],
                "level": "ut_info"
            },
            "werkzeug": {
                "handlers": ["file_handler"],
                "level": "ut_info"
            }
        },
        "root": {
            "handlers": ["file_handler"]
        }
    }

    # Test create config dict when log level is DEBUG.
    ut_format = "%(asctime)s - [%(levelname)s] - " + \
        "file: %(pathname)s - line: %(lineno)s - %(message)s"
    ret = create_log_config_dict("ut_path", "ut_debug")
    assert ret == {
        "version": 1,
        "formatters": {
            "standard": {
                "format": ut_format,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "ut_path",
                "formatter": "standard",
                "maxBytes": 1000000,
                "backupCount": 3,
                "encoding": "utf-8",
            }
        },
        "loggers": {
            "app_logger": {
                "handlers": ["file_handler"],
                "level": "ut_debug"
            },
            "werkzeug": {
                "handlers": ["file_handler"],
                "level": "ut_debug"
            }
        },
        "root": {
            "handlers": ["file_handler"]
        }
    }


@patch(f"{TEST_MODULE}.os")
@patch(f"{TEST_MODULE}.logging")
@patch(f"{TEST_MODULE}.dictConfig")
@patch(f"{TEST_MODULE}.create_log_config_dict")
def test_config_log(config_dict_mock,
                    config_mock,
                    logging_mock,
                    os_mock):
    # Mock
    mock_debug = PropertyMock(return_value="ut_debug")
    mock_info = PropertyMock(return_value="ut_info")
    type(logging_mock).DEBUG = mock_debug
    type(logging_mock).INFO = mock_info

    config_dict_mock.return_value = "ut_dict"

    os_mock.path.dirname.return_value = "ut_dirname"
    os_mock.path.join.side_effect = ["ut_path", "ut_log_path"]
    os_mock.environ.get.return_value = "ut_log_dir"

    # Test debug mode is true, and log dir exists
    config_log(True)

    os_mock.environ.get.assert_called_once_with(
        "log", "ut_path")
    os_mock.path.join.assert_has_calls([
        call("ut_dirname", "log"),
        call("ut_log_dir", "v2xvirtual-admin.log")
    ])
    assert os_mock.path.join.call_count == 2
    os_mock.stat.assert_called_once_with("ut_log_dir")
    os_mock.makedirs.assert_not_called()

    config_dict_mock.assert_called_once_with(
        "ut_log_path", "ut_debug")

    config_mock.assert_called_once_with("ut_dict")

    # Test debug mode is False, and log dir doesn't exist
    # Reset mock
    config_dict_mock.reset_mock()
    config_dict_mock.return_value = "ut_dict"
    os_mock.reset_mock()
    os_mock.path.dirname.return_value = "ut_dirname"
    os_mock.path.join.side_effect = ["ut_path", "ut_log_path"]
    os_mock.environ.get.return_value = "ut_log_dir"
    os_mock.stat.side_effect = Exception("ut_error")
    config_mock.reset_mock()

    config_log(False)

    os_mock.environ.get.assert_called_once_with(
        "log", "ut_path")
    os_mock.path.join.assert_has_calls([
        call("ut_dirname", "log"),
        call("ut_log_dir", "v2xvirtual-admin.log")
    ])
    assert os_mock.path.join.call_count == 2
    os_mock.stat.assert_called_once_with("ut_log_dir")
    os_mock.makedirs.assert_called_once_with(
        "ut_log_dir", exist_ok=True)

    config_dict_mock.assert_called_once_with(
        "ut_log_path", "ut_info")

    config_mock.assert_called_once_with("ut_dict")

    # Test raises LoggingConfigurationError
    config_dict_mock.reset_mock()
    config_dict_mock.return_value = "ut_dict"
    os_mock.reset_mock()
    os_mock.path.dirname.return_value = "ut_dirname"
    os_mock.path.join.side_effect = ["ut_path", "ut_log_path"]
    os_mock.environ.get.return_value = "ut_log_dir"
    config_mock.reset_mock()
    os_mock.stat.side_effect = None
    config_mock.reset_mock()
    config_mock.side_effect = Exception("ut_error")

    try:
        config_log(False)
    except LoggingConfigurationError as err:
        assert str(err) == "Falied to configure logging."
        assert err.error_info == "ut_error"
