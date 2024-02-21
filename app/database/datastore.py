from flask import Flask
from flask_security import MongoEngineUserDatastore, hash_password
from mongoengine import connect

import const as app_const
from database.models.auth import Role, User
from errors.app_errors import (AdminRoleCreateError, AdminUserCreateError,
                               DatastoreInitError)


def init_datastore() -> MongoEngineUserDatastore:
    """
    Connect to the database, create a MongoEngineUserDatastore instance.

    :retrun: A MongoEngineUserDatastore instance.
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
        print(err)
        raise DatastoreInitError(message=f"Failed to connect MongoDB. {err}")

    return user_datastore


def create_admin_role(user_datastore: MongoEngineUserDatastore) -> None:
    """
    Create admin role.

    :param user_datastore: MongoEngineUserDatastore object.
    :raises AdminRoleCreateError: Failed to create admin role.
    """
    try:
        user_datastore.find_or_create_role(
            name="admin", permissions=["admin-write", "admin-read"])
    except Exception as err:
        print(f"{err}")
        raise AdminRoleCreateError(message="Failed to create Admin role.",
                                   error_details=f"{err}")


def create_admin_user(user_datastore: MongoEngineUserDatastore) -> None:
    """
    Create admin user.

    :param user_datastore: MongoEngineUserDatastore object.
    :raises AdminUserCreateError: Failed to create admin user.
    """
    try:
        if not user_datastore.find_user(username="admin"):
            user_datastore.create_user(username="admin",
                                       password=hash_password("password"),
                                       roles=["admin"])
    except Exception as err:
        raise AdminUserCreateError(message="Failed to create Admin user.",
                                   error_details=f"{err}")


def create_admin_role_and_user(app: Flask):
    """
    Creates Admin role and user.
    """
    with app.app_context():
        create_admin_role(app.security.datastore)
        create_admin_user(app.security.datastore)
