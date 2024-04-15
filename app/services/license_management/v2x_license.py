import logging
import os
import re
from datetime import datetime
from typing import List, Optional

import errors.license_errors as lic_errors
from const import APP_LOGGER, LICENSE_FILE_NAME, LICENSE_FOLDER

LOG = logging.getLogger(APP_LOGGER)

# DEV_LICENSE_PATH = os.path.join(
#     os.path.dirname(__file__), DEV_LICENSE_FOLDER)

# LICENSE_PATH = os.environ.get("LICENSE_PATH", DEV_LICENSE_PATH)

LICENSE_PATH = LICENSE_FOLDER

INCREMENT_WITH_WHITESPACE = "INCREMENT "
NAME_REGEXP = re.compile(r"[\w-]*")
TIME_REGEXP = re.compile(r"([\d]+\-[a-z]+\-[\d]{4})")
VENDOR_REGEXP = re.compile(r'VENDOR_STRING="NAME=([\w ]+)[;]{1}')


class V2xLicense(object):
    """
    This class is used to store the V2X Virtual license information.
    """

    def __init__(self, name: str, start: str, expiration: str):
        """
        This function sets the name, start, and expiration properties.

        :param name: Name of the license.
        :param start: Start time of the license.
        :param expiration: Expiration date of the license.
        """

        self.__name = name
        self.__start = start
        self.__expiration = expiration

    @property
    def name(self) -> str:
        return self.__name

    @property
    def start(self) -> str:
        return self.__start

    @property
    def expiration(self) -> str:
        return self.__expiration

    def to_dict(self) -> dict:
        return {
            "name": self.__name,
            "start": self.__start,
            "expiration": self.__expiration
        }


class LicenseFile:
    """
    This is the V2X Virtual license file class.
    """

    def __init__(self):
        self.file_path: str = os.path.join(LICENSE_PATH, LICENSE_FILE_NAME)
        self.content: Optional[str] = None
        self.licenses: List[V2xLicense] = []

    def read(self) -> None:
        """
        Read the V2X Virtual license file.
        """

        try:
            with open(self.file_path, encoding="utf-8") as f:
                self.content = f.read()

        except Exception as err:
            msg = "Failed to read V2X Virtual license file."
            LOG.exception(f"{msg} {err}")
            raise lic_errors.LicenseFileReadError(
                message=msg,
                error_details=str(err))

    def write(self) -> None:
        """
        Placeholder function for uploading V2X Virtual license file.
        """

        raise NotImplementedError

    def parse(self) -> None:
        """
        Parse the content of the V2X Virtual license file,
        extract the name, start time, and expiration date.
        """

        if self.content is None:
            return

        for license in self.content.split(INCREMENT_WITH_WHITESPACE):
            formatted_license = \
                license.replace('\n', '').replace('\t', '').replace('\\', '')

            match_name = NAME_REGEXP.match(formatted_license)
            if match_name:
                name = match_name.group(0)

            start_and_expiration = TIME_REGEXP.findall(formatted_license)
            vendor = VENDOR_REGEXP.search(formatted_license)

            if start_and_expiration and (name or vendor):
                license_name = vendor.group(1) \
                    if vendor else name.replace("_", " ").replace("-", " ")

                try:
                    start = _convert_date_format(start_and_expiration[1])
                    expiration = _convert_date_format(start_and_expiration[0])

                    self.licenses.append(
                        V2xLicense(license_name, start, expiration))

                except Exception as err:
                    LOG.info(f"Failed to parse V2X Virtual License. {err}")

            else:
                # Ignore any lines that do not contain
                # the name, vendor, start, and expiration information.
                continue


def _convert_date_format(input_string: str) -> str:
    """
    Converts the date format from '01-may-2023' to '2023.05.01'.

    :param input_string: Input date string.
    :return: Desired date string format.
    """

    try:
        input_date = datetime.strptime(input_string, "%d-%b-%Y")

        output_date_string = input_date.strftime("%Y.%m.%d")

        return output_date_string

    except Exception as err:
        msg = f"Invalid date format: {input_string}."
        LOG.exception(f"{msg} {err}")
        raise lic_errors.DateFormatError(
            message=msg,
            error_details=str(err))
