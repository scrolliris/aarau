# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase


class Application(CardinalBase):
    id = PrimaryKeyField()
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    deleted_at = DateTimeField(null=True)

    class Meta:
        table_name = 'applications'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Application)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Application, cascade=True)
