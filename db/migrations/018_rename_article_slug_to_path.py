# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    migrator.rename_column('articles', 'slug', 'path')


def rollback(migrator, _database, **_kwargs):
    migrator.rename_column('articles', 'path', 'slug')
