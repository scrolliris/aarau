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
    id = PrimaryKeyField()
    parent = ForeignKeyField(
        model='self', column_name='parent_id', field='id',
        backref='children', null=True, index=True)
    notation = CharField(max_length=64, null=False)
    name = CharField(max_length=128, null=False)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'classifications'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Classification)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Classification, cascade=True)
