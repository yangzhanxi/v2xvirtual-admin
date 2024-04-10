import logging

from flask import Blueprint, session
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted

from const import ADMIN_ROLE, APP_LOGGER
from services.network_management.network_mgmt_handler import (part_num_handler,
                                                              ports_handler)

LOG = logging.getLogger(APP_LOGGER)

net = Blueprint("network", __name__)


@net.get("/ports")
@jwt_required()
@roles_accepted(ADMIN_ROLE)
def get_licenses():
    """
    GET ports view.
    """
    session.permanent = True

    return ports_handler()


@net.get("/partnum")
@jwt_required()
@roles_accepted(ADMIN_ROLE)
def get_part_num():
    """
    GET part num view.
    """
    session.permanent = True

    return part_num_handler()
