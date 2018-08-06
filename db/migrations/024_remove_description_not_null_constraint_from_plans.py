# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    migrator.drop_not_null('plans', 'description')


def rollback(migrator, _database, **_kwargs):
    migrator.add_not_null('plans', 'description')
