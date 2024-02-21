from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, request, session
from flask_jwt_extended import create_access_token, jwt_required
from flask_security import (login_required, login_user, logout_user,
                            verify_password)

import services.authentication.responses as auth_response
from const import PASSWORD_KEY, USER_NAME_KEY

auth = Blueprint("auth", __name__)


# Login endpoint
@auth.post("/login")
def login():
    # Login handler
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
        msg = "Cannot find the user."
        if "Connection refused" in str(err):
            msg = msg + ' MongoDB connection refused.'

        return ({"msg": msg},
                HTTPStatus.INTERNAL_SERVER_ERROR)

    if user and verify_password(password, user.password):
        if '_user_id' in session and session['_user_id'] == user.get_id():
            return auth_response.ALREADY_LOGGED_IN

        login_user(user)
        access_token = create_access_token(identity=username)

        return jsonify(msg="Login successfully.",
                       username=user.username,
                       access_toke=access_token)

    return auth_response.INVALID_USER_PASSWORD


@auth.post("/logout")
@jwt_required()
@login_required
def logout():
    a = logout_user()
    print(a)
    return jsonify(message="Logged out successfully"), 200
