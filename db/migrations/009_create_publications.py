# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase


class Classification(CardinalBase):
    class Meta:
        table_name = 'classifications'


class License(CardinalBase):
    class Meta:
        table_name = 'licenses'


class Publication(CardinalBase):
    id = PrimaryKeyField()
    classification = ForeignKeyField(
        model=Classification, column_name='classification_id', field='id',
        backref='publications', null=False, index=True)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    license = ForeignKeyField(
        model=License, column_name='license_id', field='id',
        backref='publications', null=True, index=True)
    copyright = CharField(max_length=64, null=False)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    deleted_at = DateTimeField(null=True)

    class Meta:
        table_name = 'publications'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Publication)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Publication, cascade=True)
