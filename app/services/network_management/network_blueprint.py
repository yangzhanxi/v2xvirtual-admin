import logging

from flask import Blueprint, session
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted

from const import ADMIN_ROLE, APP_LOGGER

LOG = logging.getLogger(APP_LOGGER)

lic = Blueprint("network", __name__)


@lic.get("/ports")
@jwt_required()
@roles_accepted(ADMIN_ROLE)
def get_licenses():
    """
    GET ports view.
    """
    session.permanent = True
    return _get_ports()


def _get_ports():
    """
    GET licenses handler
    """
    # Init License File object.
    # license_file = LicenseFile()
    # try:
    #     license_file.read()
    #     license_file.parse()

    # except Exception as err:
    #     LOG.info(f"No licenses found. {err}")
    pass
    # return [lic.to_dict() for lic in license_file.licenses]
