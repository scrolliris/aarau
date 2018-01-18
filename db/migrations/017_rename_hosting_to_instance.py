# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    migrator.rename_column('sites', 'hosting_id', 'instance_id')
    migrator.rename_column('sites', 'hosting_type', 'instance_type')


def rollback(migrator, _database, **_kwargs):
    migrator.rename_column('sites', 'instance_id', 'hosting_id')
    migrator.rename_column('sites', 'instance_type', 'hosting_type')
