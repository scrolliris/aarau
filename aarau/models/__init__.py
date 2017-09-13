""" Models handle database objects
"""
from urllib.parse import urlparse, parse_qs

from playhouse.pool import PooledPostgresqlDatabase

PooledPostgresqlDatabase.register_fields({'enum': 'enum'})


class DB(dict):
    """Database connections
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# pylint: disable=invalid-name
db = DB({  # proxies
    'cardinal': PooledPostgresqlDatabase(None, threadlocals=True),
    'analysis': PooledPostgresqlDatabase(None, threadlocals=True)
})


# pylint: disable=wrong-import-position
from .application import Application
from .article import Article
from .contribution import Contribution
from .classification import Classification
from .license import License
from .membership import Membership
from .page import Page
from .plan import Plan
from .project import Project
from .publication import Publication
from .site import Site, DeferredProject
from .user import User
from .user_email import UserEmail
from .reading_result import ReadingResult

DeferredProject.set_model(Project)

__all__ = (
    'Project', 'Membership', 'Plan',
    'Site',
    'Publication', 'Article', 'Classification', 'License', 'Contribution',
    'Application', 'Page',
    'User', 'UserEmail',
    # analysis
    'ReadingResult',
)


def init_db(settings, db_kind):
    """Initializes database connection.
    """
    key_prefix = 'database.{}.'.format(db_kind)
    url = urlparse(settings[key_prefix + 'url'])
    host = url.hostname
    if not host and not url.port:
        # check `host` query for connection via unix socket
        q = parse_qs(url.query)
        if 'host' in q:
            host = q['host'][0]

    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connect
    db[db_kind].init(
        url.path[1:],
        user=url.username,
        password=url.password,
        host=host,
        port=url.port,
        client_encoding=(settings[key_prefix + 'client_encoding'] or 'utf8'),
        max_connections=(settings[key_prefix + 'max_connections'] or 20),
        stale_timeout=(settings[key_prefix + 'stale_timeout'] or 300)
    )
    return db[db_kind]


def includeme(config):
    """Model module interface evaluated at include.

    ``config.include('aarau.models')``.
    """
    settings = config.get_settings()

    # pylint: disable=redefined-outer-name
    db['cardinal'] = init_db(settings, 'cardinal')
    db['analysis'] = init_db(settings, 'analysis')

    # this makes request.db available for use in Pyramid
    config.add_request_method(
        lambda r: db,
        'db',
        reify=True
    )
