# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    # fix wrong index name and unique constraint

    # `drop_index` from peewee_migrate (1.0.0) + peewee v3 will fail.
    # migrator.drop_index('articles', 'slug')
    sql = "DROP INDEX IF EXISTS articles_slug;"
    migrator.sql(sql)
    migrator.add_index('articles', 'path', unique=False)


def rollback(migrator, _database, **_kwargs):
    # migrator.drop_index('articles', 'path')
    sql = "DROP INDEX IF EXISTS articles_path;"
    migrator.sql(sql)

    # It does like below: (can't run it, because `slug` already doesn't exist)
    # migrator.add_index('articles', 'slug', unique=True)
    sql = "CREATE UNIQUE INDEX articles_slug on articles (path);"
    migrator.sql(sql)
