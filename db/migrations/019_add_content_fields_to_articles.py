# pylint: disable=C,R
from peewee import (
    DateTimeField,
    TextField,
)


def migrate(migrator, _database, **_kwargs):
    migrator.add_fields(
        'articles',
        content=TextField(null=True, index=False),
        content_html=TextField(null=True, index=False),
        content_updated_at=DateTimeField(null=True, default=None),
    )


def rollback(migrator, _database, **_kwargs):
    migrator.remove_fields('articles', *[
        'content',
        'content_html',
        'content_updated_at',
    ], cascade=True)
