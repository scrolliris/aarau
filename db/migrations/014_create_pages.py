# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase, EnumField


class Application(CardinalBase):
    class Meta:
        db_table = 'applications'


class Page(CardinalBase):
    scopes = ('public', 'private')

    id = PrimaryKeyField()
    application = ForeignKeyField(
        rel_model=Application, db_column='application_id', to_field='id',
        related_name='pages', null=False, index=True)
    code = CharField(max_length=128, null=False, unique=True, index=True)
    path = CharField(max_length=255, null=False, unique=True, index=True)
    title = CharField(max_length=255, null=False)
    scope = EnumField(
        choices=scopes,
        null=False, index=True, default='public')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)
    deleted_at = DateTimeField(null=True)

    class Meta:
        db_table = 'pages'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Page)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Page, cascade=True)
