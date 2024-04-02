# The MongoDB info.
DB_NAME = "v2x_admin"
DB_HOST = "mongodb://localhost"
DB_PORT = 27017

# The root user of MongoDB.
ROOT = "root"
ROOT_PASSWORD = "example"

# Administrator information of V2x Virtual Admin app
ADMIN_USER = "admin"
ADMIN_ROLE = "admin"
ADMIN_PASSWORD = "password"
ADMIN_PERMISSIONS = ["admin-write", "admin-read"]

# Generated by secrets.SystemRandom().getrandbits(128)))
SECURITY_PASSWORD_SALT = "329072734491176369717098496818781888587"

# Parameters for the HTTP request.
USER_NAME_KEY = "username"
PASSWORD_KEY = "password"

# Dev license file info
DEV_LICENSE_FOLDER = "license_file"
LICENSE_FILE_NAME = "license.lic"
# LICENSE_FOLDER = r"/mnt/spirent/ttwb/flexnet"

# Log file dir
LOG_FILE_DIR = "log"
LOG_FILE_NAME = "v2xvirtual-admin.log"

APP_LOGGER = "app_logger"

STC_SESSION_PN_MAPPING = {
    ""
}

PN_PORT_MAPPING = {
    "SPT-M1": [
        "slot7port1",
        "slot7port2",
        "slot7port3",
        "slot7port4"
    ],
    "SPT-C50": [
        "slot1port1",
        "slot1port2",
        "slot1port3",
        "slot1port4"
    ]
}

STC_SERVER = "127.0.0.1"
STC_SERVER_PORT = 8888

STC_SESSION_PREFIX = "TTwb_"
STC_SESSION_SUFFIX = " - ttwb"
