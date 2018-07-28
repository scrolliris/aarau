# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase, EnumField


class User(CardinalBase):
    class Meta:
        table_name = 'users'


class UserEmail(CardinalBase):
    activation_states = ('pending', 'active')
    types = ('primary', 'normal')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        model=User, column_name='user_id', field='id',
        backref='emails', null=False, index=True)
    email = CharField(max_length=64, null=False, unique=True, index=True)
    type = EnumField(
        choices=types, null=False, index=True, default='normal')

    activation_state = EnumField(
        choices=activation_states,
        null=False, index=True, default='pending')
    activation_token = CharField(max_length=255, null=True, index=True)
    activation_token_expires_at = DateTimeField(
        null=True, default=None)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'user_emails'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(UserEmail)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(UserEmail, cascade=True)
