# pylint: disable=invalid-name
from peewee import (
    CharField,
)


def migrate(migrator, _database, **_kwargs):
    migrator.add_fields(
        'sites',
        slug=CharField(max_length=255, null=True, index=True),
    )


def rollback(migrator, _database, **_kwargs):
    migrator.drop_index('sites', 'slug')
    migrator.remove_fields('sites', *['slug'], cascade=True)
