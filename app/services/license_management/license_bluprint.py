import logging

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_security import login_required, roles_accepted

from services.license_management.v2x_license import LicenseFile

LOG = logging.getLogger()

lic = Blueprint("license", __name__)


@lic.get("/licenses")
@jwt_required()
@login_required
@roles_accepted("admin")
def get_licenses():
    """
    Gets licenses handler.
    """
    # Init License File object.
    license_file = LicenseFile()
    try:
        license_file.read()
        license_file.parse()

    except Exception as err:
        LOG.info(f"No Licenses found. {err}")

    return [lic.to_dict() for lic in license_file.licenses]
