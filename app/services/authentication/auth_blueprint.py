import logging
from http import HTTPStatus
from typing import Set

from flask import Blueprint, current_app, jsonify, request, session
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import current_user
from flask_security import (login_required, login_user, logout_user,
                            verify_password)

import services.authentication.responses as auth_response
from const import APP_LOGGER, PASSWORD_KEY, USER_NAME_KEY

LOG = logging.getLogger(APP_LOGGER)

auth = Blueprint("auth", __name__)

LOGGED_IN_USERS: Set[str] = set()


# Login endpoint
@auth.post("/login")
def login():
    """
    This method serves as the login handler,
    responsible for managing user authentication and access control.
    """

    try:
        username, password = (
            request.json.get(USER_NAME_KEY).strip(),
            request.json.get(PASSWORD_KEY).strip(),
        )

    except Exception:
        return auth_response.INVALID_USER_PASSWORD

    if username is None or password is None:
        return auth_response.INVALID_USER_PASSWORD

    try:
        user = current_app.security.datastore.find_user(username=username)
    except Exception as err:
        msg = "Cannot find the user 1."
        if "Connection refused" in str(err):
            msg = msg + ' MongoDB connection refused.'

            return ({"msg": msg},
                    HTTPStatus.INTERNAL_SERVER_ERROR)

    if user and verify_password(password, user.password):
        login_user(user)
        access_token = create_access_token(identity=username)

        LOG.info(f"User {username} logged in successfully.")

        return jsonify(msg="Login successfully.",
                       username=user.username,
                       access_token=access_token)

    return auth_response.INVALID_USER_PASSWORD


@auth.post("/logout")
@jwt_required()
@login_required
def logout():
    """
    This method serves as the logout handler,
    responsible for handling user logout operations
    and ensuring secure session termination.
    """

    next_url = ""  # noqa
    logout_user()
    LOG.info("User logged out successfully.")

    return auth_response.LOGOUT_SUCCEED


@auth.get("/currentuser")
@jwt_required()
@login_required
def get_current_user():
    """
    Gets name of current user.
    """

    next_url = ""  # noqa
    user = current_user
    if user:
        return jsonify(username=user.username)

    return jsonify(username='')
