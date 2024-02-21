import os
import re
from typing import List

# FIXME: Use the license.lic path
LICENSE_PATH = os.path.join(
    os.path.dirname(__file__), "license_file")
LICENSE_FILE_NAME = "license.lic"
LICENSE_PATH = os.path.join(LICENSE_PATH)

INCREMENT_WITH_WHITESPACE = "INCREMENT "
NAME_REGEXP = re.compile(r"[\w-]*")
TIME_REGEXP = re.compile(r"([\d]+\-[a-z]+\-[\d]{4})")
VENDOR_REGEXP = re.compile(r'VENDOR_STRING="NAME=([\w ]+)[;]{1}')


class V2xLicense(object):
    """
    This class is used for storing the V2X license information.

    Attributes:
        name: Name of the license.
        start: The start time of the license.
        expiration: The expriation data of the license.
    """

    def __init__(self, name: str, start: str, expiration: str):
        """
        This function sets the name, start and expiration properties.

        Args:
            name: (str): Name of the license.
            start: (str): Start time of the license.
            expiration (str): Expriation data of the license.
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

    def to_json(self):
        return {
            "name": self.__name,
            "start": self.__start,
            "expiration": self.__expiration
        }


class LicenseFile(object):
    """
    This is the V2X license file class.
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
                print(self.content)
        except Exception as err:
            print(f"Failed to open license file. {err}")

    def write(self):
        """
        Placeholder function for upload file.
        """
        pass

    def parse(self):
        """
        Parse the content of license.lic file, extract the name, start time,
        and expiration data.
        """
        for license in self.content.split(INCREMENT_WITH_WHITESPACE):
            # if (license.find('START') < 0):
            #     # Skip the content doesn't contain the word START
            #     continue

            formatted_license = \
                license.replace('\n', '').replace('\t', '').replace('\\', '')
            # print(formatted_license)
            name = NAME_REGEXP.match(formatted_license).group(0)
            start_and_expiration = TIME_REGEXP.findall(formatted_license)
            vendor = VENDOR_REGEXP.search(formatted_license)

            if start_and_expiration and (name or vendor):
                license_name = vendor.group(1) \
                    if vendor else name.replace("_", " ").replace("-", " ")

                self.licenses.append(
                    V2xLicense(license_name,
                               start_and_expiration[0],
                               start_and_expiration[1]))
            else:
                continue
