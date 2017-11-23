# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    migrator.drop_not_null('sites', 'domain')
    migrator.add_index('sites', *['domain'], unique=False)


def rollback(migrator, _database, **_kwargs):
    migrator.drop_index('sites', 'domain')
    migrator.add_not_null('sites', 'domain')
