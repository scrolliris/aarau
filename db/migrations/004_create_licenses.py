# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase


class License(CardinalBase):
    id = PrimaryKeyField()
    identifier = CharField(max_length=32, null=False, unique=True, index=True)
    fullname = CharField(max_length=64, null=False)
    url = CharField(max_length=128, null=False)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'licenses'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(License)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(License, cascade=True)
