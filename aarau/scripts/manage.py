import os
import re
import sys
from contextlib import contextmanager

from pyramid.paster import get_appsettings, setup_logging

from aarau import resolve_env_vars
from aarau.env import load_dotenv_vars
from aarau.models import (
    Project, Membership, Plan,
    Site,
    Publication, Article, Classification, ClassificationHierarchy,
    License, Contribution,
    Application, Page,
    User, UserEmail,
)
from aarau.yaml import (
    yaml_loader,
    tokenize,
    set_password
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <command> <action> [var=value]\n'
          '(example: "%s \'development.ini#\' db [ACTION-NAME]")' % (cmd, cmd))
    sys.exit(1)


class CLI():
    """Command line interface to manage database (PostgreSQL)."""

    def __init__(self, settings):
        self.settings = settings

        # for migrate router
        self.migrate_table = 'migrations'
        self.migrate_dir = os.path.join(os.getcwd(), 'db', 'migrations')

    @contextmanager
    def _raw_db(self, kind):
        from copy import copy
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        with self._db(kind) as db:
            datname = copy(db.database)
            db.database = 'template1'
            conn = db.connection()
            conn.set_isolation_level(
                ISOLATION_LEVEL_AUTOCOMMIT
            )
            yield (db, datname)

    @contextmanager
    def _db(self, kind):
        from aarau.models import db, init_db

        db[kind] = init_db(self.settings, kind)

        yield db[kind]

    def help(self, _):  # pylint: disable=no-self-use
        print('usage: db {help|init|seed|drop} [var=value]')
        sys.exit(1)

    def init(self, _):
        """Initializes database."""
        if 'ENV' not in os.environ or \
           os.environ['ENV'] not in ('development', 'test'):
            print("Run in {development,test}")
            sys.exit(1)

        with self._raw_db('cardinal') as (db, datname):
            q = "SELECT 1 FROM pg_database WHERE datname='{}'".format(datname)
            if db.execute_sql(q).rowcount != 0:
                sys.exit(0)

            q = "CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(
                datname,
                'UTF-8',
                'template0'
            )
            db.execute_sql(q)

    def migrate(self, _):
        """Migrates database schema."""
        from peewee_migrate import Router

        with self._db('cardinal') as db, db.atomic():
            router = Router(db, migrate_table=self.migrate_table,
                            migrate_dir=self.migrate_dir)
            router.run()

    def rollback(self, _):
        """Rollbacks a latest migration."""
        from peewee_migrate import Router

        with self._db('cardinal') as db, db.atomic():
            router = Router(db, migrate_table=self.migrate_table,
                            migrate_dir=self.migrate_dir)
            if router.done:
                router.rollback(router.done[-1])

    def seed(self, args):
        """Imports db seed records for development."""
        with self._db('cardinal') as db, db.atomic():
            with yaml_loader(self.settings) as loader:
                def load_data(klass, attrs):
                    with tokenize(attrs) as (tokens, attributes):

                        obj = klass(**attributes)
                        obj.save()

                        with set_password(obj, attributes) as obj:
                            obj.save()

                            for k, f in tokens.items():
                                setattr(obj, k, f(obj))
                                obj.save()

                # db/seeds/*.yml
                # TODO: import all files in db/seeds/*.yml
                # `order` sensitive
                models = [
                    Plan, Classification, ClassificationHierarchy, License,
                    Project,
                    Publication, Article,
                    Application, Page,
                    Site,
                    User, UserEmail, Membership, Contribution,
                ]

                for model in models:
                    # pylint: disable=no-member,protected-access
                    table = model._meta.table_name
                    seeds_dir = os.path.join(os.getcwd(), 'db', 'seeds')
                    files = [f for f in os.listdir(seeds_dir) if
                             f.startswith(table) and f.endswith('.yml') and
                             'sample' not in f]

                    # e.g. aarau_manage db seed plans.yml plans.1.yml
                    if args:
                        files = list(filter(lambda f: f in args, files))

                    # e.g. classification.yml, classification.1.yml...
                    for f in sorted(files, key=(lambda v: int(
                            re.sub(r'[a-z\_]', '', v).replace('.', '0')))):
                        seed_yml = os.path.join(seeds_dir, f)
                        if os.path.isfile(seed_yml):
                            print(os.path.basename(seed_yml))
                            data = loader(seed_yml)
                            for attributes in data[table]:
                                load_data(model, attributes)

    def truncate(self, args):
        """Truncates a (master data) table."""
        if not args or len(args) != 1:
            print("Specify only a table as an arg")
            sys.exit(1)

        table = args[0]
        # only master data tables
        if table not in ('plans', 'classifications', 'licenses'):
            print("Table not found")
            sys.exit(1)

        with self._db('cardinal') as db, db.atomic():
            q = 'TRUNCATE table {0:s} CASCADE'.format(table)
            db.execute_sql(q)

    def drop(self, _):
        """Drops entire database."""
        if 'ENV' not in os.environ or \
           os.environ['ENV'] not in ('development', 'test'):
            print("Run in {development,test}")
            sys.exit(1)

        with self._raw_db('cardinal') as (db, datname):
            q = "SELECT 1 FROM pg_database WHERE datname='{}'".format(datname)
            if db.execute_sql(q).rowcount == 0:
                sys.exit(0)

            q = 'DROP DATABASE {0}'.format(datname)
            db.execute_sql(q)


def main(argv=None):
    if not argv:
        argv = sys.argv

    if len(argv) < 4:
        usage(argv)
    config_uri = argv[1]
    command = argv[2]
    action = argv[3]
    args = argv[4:]

    setup_logging(config_uri)
    load_dotenv_vars()

    if command not in ('db',):
        raise Exception('Run with valid command {db} :\'(')
    else:
        actions = ('help', 'init', 'drop', 'migrate', 'rollback',
                   'seed', 'truncate')
        if action not in actions:
            err_msg = 'Run with valid action {0!s} :\'('
            raise Exception(err_msg.format('|'.join(actions)))

    settings = get_appsettings(config_uri)
    settings = resolve_env_vars(dict(settings))

    cli = CLI(settings)
    getattr(cli, action.lower())(args)
