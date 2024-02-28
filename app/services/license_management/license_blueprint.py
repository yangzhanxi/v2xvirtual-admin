import logging

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_security import login_required, roles_accepted

from const import ADMIN_ROLE
from services.license_management.v2x_license import LicenseFile

LOG = logging.getLogger()

lic = Blueprint("license", __name__)


@lic.get("/licenses")
@jwt_required()
@login_required
@roles_accepted(ADMIN_ROLE)
def get_licenses():
    """
    GET licenses view.
    """
    return _get_licenses()


def _get_licenses():
    """
    GET licenses handler
    """
    # Init License File object.
    license_file = LicenseFile()
    try:
        license_file.read()
        license_file.parse()

    except Exception as err:
        LOG.info(f"No licenses found. {err}")

    return [lic.to_dict() for lic in license_file.licenses]
