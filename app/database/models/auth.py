from flask_security import RoleMixin, UserMixin
from mongoengine import Document, fields

from const import DB_NAME


class Role(Document, RoleMixin):
    name = fields.StringField(max_length=80, uniquie=True)
    description = fields.StringField(max_length=255)
    permissions = fields.ListField(required=False)
    meta = {"db_alias": DB_NAME}


class User(Document, UserMixin):
    username = fields.StringField(max_length=80, unique=True)
    password = fields.StringField(max_length=255)
    active = fields.BooleanField(default=True)
    fs_uniquifier = fields.StringField(max_length=64, unique=True)
    roles = fields.ListField(fields.ReferenceField(Role), default=[])
    meta = {"db_alias": DB_NAME}
