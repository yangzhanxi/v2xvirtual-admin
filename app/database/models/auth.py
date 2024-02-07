from flask_mongoengine import Document
from mongoengine import fields


class Role(Document):
    name = fields.StringField(max_length=80, uniquie=True)


class User(Document):
    username = fields.StringField(max_length=80, unique=True)
    password = fields.StringField(max_length=255)
    rolse = fields.ReferenceField(Role)
