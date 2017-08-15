# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import Base


class Classification(Base):
    id = PrimaryKeyField()
    parent = ForeignKeyField(
        rel_model='self', db_column='parent_id', to_field='id',
        related_name='children', null=True, index=True)
    notation = CharField(max_length=64, null=False)
    name = CharField(max_length=128, null=False)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        db_table = 'classifications'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Classification)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Classification, cascade=True)
