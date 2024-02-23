from http import HTTPStatus

INVALID_USER_PASSWORD = \
    ({"msg": "Invalid username or password."}, HTTPStatus.UNPROCESSABLE_ENTITY)

UNAUTHORIZED = \
    ({"msg": "Wrong credential."}, HTTPStatus.UNAUTHORIZED)

ALREADY_LOGGED_IN = \
    ({"msg": "User is already logged in."}, HTTPStatus.OK)

LOGOUT_SUCCEED = \
    ({"msg": "Logged out successfully."}, HTTPStatus.OK)
