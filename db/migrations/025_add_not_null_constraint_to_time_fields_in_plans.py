# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    migrator.add_not_null('plans', 'created_at')
    migrator.add_not_null('plans', 'updated_at')


def rollback(migrator, _database, **_kwargs):
    migrator.drop_not_null('plans', 'created_at')
    migrator.drop_not_null('plans', 'updated_at')
