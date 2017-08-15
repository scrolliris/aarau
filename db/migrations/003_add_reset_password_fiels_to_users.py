# pylint: disable=C,R
from peewee import (
    CharField,
    DateTimeField,
)


def migrate(migrator, _database, **_kwargs):
    migrator.add_fields(
        'users',
        reset_password_token=CharField(max_length=255, null=True, index=True),
        reset_password_token_expires_at=DateTimeField(null=True, default=None),
        reset_password_token_sent_at=DateTimeField(null=True, default=None),
    )


def rollback(migrator, _database, **_kwargs):
    migrator.drop_index('users', 'reset_password_token')
    migrator.remove_fields('users', *[
        'reset_password_token',
        'reset_password_token_expires_at',
        'reset_password_token_sent_at',
    ], cascade=True)
