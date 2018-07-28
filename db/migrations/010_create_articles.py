# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase, EnumField


class Publication(CardinalBase):
    class Meta:
        table_name = 'publications'


class License(CardinalBase):
    class Meta:
        table_name = 'licenses'


class Article(CardinalBase):
    scopes = ('public', 'private')
    progress_states = (
        'draft', 'wip', 'ready', 'accepted', 'scheduled', 'published',
        'rejected', 'archived')

    id = PrimaryKeyField()
    publication = ForeignKeyField(
        model=Publication, column_name='publication_id', field='id',
        backref='articles', null=False, index=True)
    code = CharField(max_length=128, null=False, unique=True, index=True)
    slug = CharField(max_length=255, null=False, unique=True, index=True)
    title = CharField(max_length=255, null=False)
    license = ForeignKeyField(
        model=License, column_name='license_id', field='id',
        backref='articles', null=True, index=True)
    copyright = CharField(max_length=64, null=False)
    scope = EnumField(
        choices=scopes,
        null=False, index=True, default='public')
    progress_state = EnumField(
        choices=progress_states,
        null=False, index=True, default='draft')

    published_at = DateTimeField(null=True)
    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)
    deleted_at = DateTimeField(null=True)

    class Meta:
        table_name = 'articles'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Article)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Article, cascade=True)
