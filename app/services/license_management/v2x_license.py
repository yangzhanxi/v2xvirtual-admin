import os
import re
from datetime import datetime
from typing import List

import errors.license_errors as lic_errors
from const import DEV_LICENSE_FOLDER, LICENSE_FILE_NAME

# FIXME: Use the license.lic path
DEV_LICENSE_PATH = os.path.join(
    os.path.dirname(__file__), DEV_LICENSE_FOLDER)

LICENSE_PATH = os.environ.get("LICENSE_PATH", DEV_LICENSE_PATH)

INCREMENT_WITH_WHITESPACE = "INCREMENT "
NAME_REGEXP = re.compile(r"[\w-]*")
TIME_REGEXP = re.compile(r"([\d]+\-[a-z]+\-[\d]{4})")
VENDOR_REGEXP = re.compile(r'VENDOR_STRING="NAME=([\w ]+)[;]{1}')


class V2xLicense(object):
    """
    This class is used for storing the V2X Virtual license information.
    """

    def __init__(self, name: str, start: str, expiration: str):
        """
        This function sets the name, start and expiration properties.

        :param name: Name of the license.
        :param start: Start time of the license.
        :param expiration: Expriation data of the license.
        """

        self.__name = name
        self.__start = start
        self.__expiration = expiration

    @property
    def name(self) -> str:
        return self.__name

    @property
    def start(self):
        return self.__start

    @property
    def expiration(self):
        return self.__expiration

    def to_dict(self):
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
        self.content: str = None
        self.licenses: List[V2xLicense] = []

    def read(self):
        """
        Read license file.
        """

        try:
            with open(self.file_path, encoding='utf-8') as f:
                self.content = f.read()
                # FIXME: Add log
        except Exception as err:
            # FIXME: Add log
            raise lic_errors.LicenseFileReadError(
                message="Failed to read V2X Virtual license file.",
                error_details=str(err))

    def write(self):
        """
        Placeholder function for upload file.
        """
        raise NotImplementedError

    def parse(self):
        """
        Parse the content of license.lic file, extract the name, start time,
        and expiration data.
        """
        if self.content is None:
            return

        for license in self.content.split(INCREMENT_WITH_WHITESPACE):
            formatted_license = \
                license.replace('\n', '').replace('\t', '').replace('\\', '')

            name = NAME_REGEXP.match(formatted_license).group(0)
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
                    # FIXME: Add log
                    print(f"{err}")

            else:
                # Ignore any lines that do not contain
                # the name, vendor, start, and expiration information.
                continue


def _convert_date_format(input_string: str) -> str:
    """
    Converts the date formt from '01-may-2023' to '2023.05.01'.

    :param input_string: Input date string.
    :return: Desired date string format.
    """

    try:
        input_date = datetime.strptime(input_string, "%d-%b-%Y")

        output_date_string = input_date.strftime("%Y.%m.%d")

        return output_date_string

    except Exception as err:
        raise lic_errors.DateFormatError(
            message=f"Invalid date format: {input_string}.",
            error_details=str(err))
