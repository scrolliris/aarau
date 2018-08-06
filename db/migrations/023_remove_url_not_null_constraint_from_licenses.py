# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    migrator.drop_not_null('licenses', 'url')


def rollback(migrator, _database, **_kwargs):
    migrator.add_not_null('licenses', 'url')
