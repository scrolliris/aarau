from urllib.parse import urlparse, parse_qs

from .db import db

from .application import Application
from .article import Article
from .contribution import Contribution
from .classification import Classification
from .classification_hierarchy import ClassificationHierarchy
from .license import License
from .membership import Membership
from .page import Page
from .plan import Plan
from .project import Project
from .publication import Publication
from .site import Site
from .user import User
from .user_email import UserEmail
from .reading_result import ReadingResult


__all__ = (
    'Project', 'Membership', 'Plan',
    'Site',
    'Publication', 'Article', 'Classification', 'ClassificationHierarchy',
    'License', 'Contribution',
    'Application', 'Page',
    'User', 'UserEmail',
    # analysis
    'ReadingResult',
)


def init_db(settings, kind):
    """Initializes database connection."""
    prefix = 'database.{}.'.format(kind)
    url = urlparse(settings[prefix + 'url'])
    host = url.hostname
    if not host and not url.port:
        # check `host` query for connection via unix socket
        q = parse_qs(url.query)
        if 'host' in q:
            host = q['host'][0]

    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connect
    if not db[kind] or db[kind].is_closed():
        db[kind].init(
            url.path[1:],
            user=url.username,
            password=url.password,
            host=host,
            port=url.port,
            client_encoding=(settings[prefix + 'client_encoding'] or 'utf8'),
            max_connections=(settings[prefix + 'max_connections'] or 20),
            stale_timeout=(settings[prefix + 'stale_timeout'] or 300)
        )
    return db[kind]


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
