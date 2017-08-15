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
    class Meta:
        db_table = 'classifications'


class License(Base):
    class Meta:
        db_table = 'licenses'


class Publication(Base):
    id = PrimaryKeyField()
    classification = ForeignKeyField(
        rel_model=Classification, db_column='classification_id', to_field='id',
        related_name='publications', null=False, index=True)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    license = ForeignKeyField(
        rel_model=License, db_column='license_id', to_field='id',
        related_name='publications', null=True, index=True)
    copyright = CharField(max_length=64, null=False)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    deleted_at = DateTimeField(null=True)

    class Meta:
        db_table = 'publications'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Publication)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Publication, cascade=True)
