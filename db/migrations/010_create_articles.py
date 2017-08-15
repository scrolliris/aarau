# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import Base, EnumField


class Publication(Base):
    class Meta:
        db_table = 'publications'


class License(Base):
    class Meta:
        db_table = 'licenses'


class Article(Base):
    scopes = ('public', 'private')
    progress_states = (
        'draft', 'wip', 'ready', 'accepted', 'scheduled', 'published',
        'rejected', 'archived')

    id = PrimaryKeyField()
    publication = ForeignKeyField(
        rel_model=Publication, db_column='publication_id', to_field='id',
        related_name='articles', null=False, index=True)
    code = CharField(max_length=128, null=False, unique=True, index=True)
    slug = CharField(max_length=255, null=False, unique=True, index=True)
    title = CharField(max_length=255, null=False)
    license = ForeignKeyField(
        rel_model=License, db_column='license_id', to_field='id',
        related_name='articles', null=True, index=True)
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
        db_table = 'articles'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Article)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Article, cascade=True)
