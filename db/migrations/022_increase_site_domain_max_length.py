# pylint: disable=C,R


def migrate(migrator, _database, **_kwargs):
    # The `change_columns` won't work with peewee_migrate 1.0.0 (peewee v3)
    #
    # * https://github.com/klen/peewee_migrate/issues/87
    # * https://github.com/klen/peewee_migrate/pull/74/commits/5549329ea45417368897bfcf5e0364799974f45e
    #
    # ```
    # migrator.change_columns(
    #     'sites',
    #     domain=CharField(max_length=64, null=True)
    # )
    # ```
    q = 'ALTER TABLE sites' \
        ' ALTER COLUMN domain TYPE varchar(64),' \
        ' ALTER COLUMN domain SET DEFAULT NULL'
    migrator.sql(q)


def rollback(migrator, _database, **_kwargs):
    # The `change_columns` won't work with peewee_migrate 1.0.0 (peewee v3)
    #
    # * https://github.com/klen/peewee_migrate/issues/87
    # * https://github.com/klen/peewee_migrate/pull/74/commits/5549329ea45417368897bfcf5e0364799974f45e
    #
    # ```
    # migrator.change_columns(
    #     'sites',
    #     domain=CharField(max_length=32, null=True)
    # )
    # ```
    q = 'ALTER TABLE sites' \
        ' ALTER COLUMN domain TYPE varchar(32),' \
        ' ALTER COLUMN domain SET DEFAULT NULL'
    migrator.sql(q)
