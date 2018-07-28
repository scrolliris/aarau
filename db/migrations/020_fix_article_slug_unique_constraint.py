# pylint: disable=invalid-name


def migrate(migrator, _database, **_kwargs):
    # fix wrong index name and unique constraint
    migrator.migrator.drop_index('articles', 'slug')
    migrator.add_index('articles', 'path', unique=False)


def rollback(migrator, database, **_kwargs):
    migrator.migrator.drop_index('articles', 'path')
    # It does like below: (can't run it, because `slug` already doesn't exist)
    # migrator.add_index('articles', 'slug', unique=True)
    sql = "CREATE UNIQUE INDEX articles_slug on articles (path);"
    database.execute_sql(sql)
