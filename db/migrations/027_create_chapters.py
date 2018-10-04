# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase


class Publication(CardinalBase):
    class Meta:
        table_name = 'publications'


class Chapter(CardinalBase):
    id = PrimaryKeyField()
    publication = ForeignKeyField(
        model=Publication, column_name='publication_id', field='id',
        backref='chapters', null=False, index=True)
    parent = ForeignKeyField(
        model='self', column_name='parent_id', field='id',
        backref='children', null=True, index=True)
    slug = CharField(max_length=255, null=False, unique=True, index=True)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'chapters'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Chapter)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Chapter, cascade=True)
