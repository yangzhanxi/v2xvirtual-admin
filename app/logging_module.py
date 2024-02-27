import logging
import os
from logging.config import dictConfig

from const import LOG_FILE_DIR, LOG_FILE_NAME
from errors.app_errors import LoggingConfigurationError


def create_log_config_dict(file_path: str,
                           log_level: int = logging.INFO) -> dict:
    """
    Creates the logging configuration dictionary.

    :param log_level: The logger level, defaults to INFO.
    :param file_path: The name of the log file.
    :return config_dict: Logging configuration dictionary.
    """

    debug_format = "%(asctime)s - [%(levelname)s] - " + \
        "file: %(pathname)s - line: %(lineno)s - %(message)s"

    log_format = debug_format if logging.DEBUG == log_level \
        else "%(asctime)s - [%(levelname)s] - %(message)s"

    config_dict: dict = {
        "version": 1,
        "formatters": {
            "standard": {
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": file_path,
                "formatter": "standard",
                "maxBytes": 1000000,
                "backupCount": 3,
                "encoding": "utf-8",
            }
        },
        "loggers": {
            "app_logger": {
                "handlers": ["file_handler"],
                "level": log_level
            },
            "werkzeug": {
                "handlers": ["file_handler"],
                "level": log_level
            }
        },
        "root": {
            "handlers": ["file_handler"],
            # "propagate": False
        },
    }

    return config_dict


def config_log(is_debug: bool = False) -> None:
    """
    The method is used to configure logging.

    :param is_debug: Flag used to indicate whether or not it is in debug mode.
    """

    log_level = logging.DEBUG if is_debug else logging.INFO

    log_dir = os.environ.get(
        LOG_FILE_DIR,
        os.path.join(os.path.dirname(__file__), LOG_FILE_DIR))

    try:
        os.stat(log_dir)
    except Exception:
        os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(
        log_dir, LOG_FILE_NAME)

    config = create_log_config_dict(log_file_path, log_level)

    try:
        dictConfig(config)
    except Exception as err:
        raise LoggingConfigurationError(
            message="Falied to configure logging.",
            error_details=str(err))
