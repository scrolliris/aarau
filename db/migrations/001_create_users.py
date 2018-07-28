# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase, EnumField


class User(CardinalBase):
    activation_states = ('pending', 'active')

    id = PrimaryKeyField()
    name = CharField(max_length=64, null=True)
    username = CharField(max_length=32, null=True, index=True)
    email = CharField(max_length=64, null=False, unique=True, index=True)
    password = CharField(max_length=255)

    activation_state = EnumField(
        choices=activation_states,
        null=True, index=True, default='pending')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'users'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(User)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(User, cascade=True)
