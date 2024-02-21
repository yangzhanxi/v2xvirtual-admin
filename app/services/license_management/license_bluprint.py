from flask import Blueprint
# from flask_security import auth_required

from services.license_management.v2x_license import LicenseFile

lic = Blueprint("license", __name__)


@lic.get("/licenses")
# @auth_required()
def get_licenses():
    """_summary_

    Returns:
        _type_: _description_
    """
    license_file = LicenseFile()
    license_file.read()
    license_file.parse()

    return [lic.to_json() for lic in license_file.licenses]
