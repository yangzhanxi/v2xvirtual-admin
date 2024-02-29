import logging

from flask import Flask
from flask_security import MongoEngineUserDatastore, Security, hash_password
from mongoengine import connect  # type: ignore

import const as app_const
from database.models.auth import Role, User
from errors.app_errors import (AdminRoleCreateError, AdminUserCreateError,
                               DatastoreInitError)

LOG = logging.getLogger(app_const.APP_LOGGER)


def init_datastore() -> MongoEngineUserDatastore:
    """
    Connect to the database and create a MongoEngineUserDatastore instance.

    :return: A MongoEngineUserDatastore instance.
    :raises: Datastore init error.
    """

    try:
        db = connect(alias=app_const.DB_NAME,
                     db=app_const.DB_NAME,
                     username=app_const.ROOT,
                     password=app_const.ROOT_PASSWORD,
                     host=app_const.DB_HOST,
                     port=app_const.DB_PORT)
        user_datastore = MongoEngineUserDatastore(db, User, Role)
    except Exception as err:
        err_msg = "Failed to connect MongoDB."
        LOG.exception(f"{err_msg} {err}")
        raise DatastoreInitError(
            message=err_msg, error_details=str(err))

    return user_datastore


def create_admin_role(user_datastore: MongoEngineUserDatastore) -> None:
    """
    Create admin role.

    :param user_datastore: MongoEngineUserDatastore object.
    :raises AdminRoleCreateError: Failed to create admin role.
    """

    try:
        user_datastore.find_or_create_role(
            name=app_const.ADMIN_ROLE, permissions=app_const.ADMIN_PERMISSIONS)
    except Exception as err:
        msg = "Failed to create Admin role."
        LOG.exception(f"{msg} {err}")
        raise AdminRoleCreateError(message=msg,
                                   error_details=str(err))


def create_admin_user(user_datastore: MongoEngineUserDatastore) -> None:
    """
    Create admin user.

    :param user_datastore: MongoEngineUserDatastore object.
    :raises AdminUserCreateError: Failed to create admin user.
    """

    try:
        if not user_datastore.find_user(username=app_const.ADMIN_USER):
            user_datastore.create_user(
                username=app_const.ADMIN_USER,
                password=hash_password(app_const.ADMIN_PASSWORD),
                roles=[app_const.ADMIN_ROLE])
    except Exception as err:
        msg = "Failed to create Admin user."
        LOG.exception(f"{msg} {err}")
        raise AdminUserCreateError(message=msg,
                                   error_details=str(err))


def create_admin_role_and_user(app: Flask) -> None:
    """
    Creates Admin role and user.

    :param app: Flask object.
    """

    with app.app_context():
        security: Security = getattr(app, "security")
        if security:
            datastore: MongoEngineUserDatastore = \
                getattr(security, "datastore")
            if datastore:
                create_admin_role(datastore)
                create_admin_user(datastore)
