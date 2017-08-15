""" Models handle database objects
"""
from urllib.parse import urlparse, parse_qs

from playhouse.pool import PooledPostgresqlDatabase

PooledPostgresqlDatabase.register_fields({'enum': 'enum'})
# pylint: disable=invalid-name
db = PooledPostgresqlDatabase(None, threadlocals=True)

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

DeferredProject.set_model(Project)

__all__ = (
    'Project', 'Membership', 'Plan',
    'Site',
    'Publication', 'Article', 'Classification', 'License', 'Contribution',
    'Application', 'Page',
    'User', 'UserEmail'
)


def init_db(settings):
    """Initializes database connection.
    """
    url = urlparse(settings['database.url'])
    host = url.hostname
    if not host and not url.port:
        # check `host` query for connection via unix socket
        q = parse_qs(url.query)
        if 'host' in q:
            host = q['host'][0]

    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connect
    db.init(
        url.path[1:],
        user=url.username,
        password=url.password,
        host=host,
        port=url.port,
        client_encoding=(settings['database.client_encoding'] or 'utf8'),
        max_connections=(settings['database.max_connections'] or 20),
        stale_timeout=(settings['database.stale_timeout'] or 300)
    )
    return db


def includeme(config):
    """Model module interface evaluated at include.

    ``config.include('aarau.models')``.
    """
    settings = config.get_settings()

    # pylint: disable=redefined-outer-name
    db = init_db(settings)

    # this makes request.db available for use in Pyramid
    config.add_request_method(
        lambda r: db,
        'db',
        reify=True
    )
