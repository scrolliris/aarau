"""Configuration for testing
"""
# pylint: disable=redefined-outer-name,unused-argument
import os

import pytest

from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.router import Router
from webtest.app import TestApp

# NOTE:
# The request variable in py.test is special context of testing.
# See http://doc.pytest.org/en/latest/fixture.html#request-context

TEST_DIR = os.path.dirname(__file__)
INI_FILE = os.path.join(TEST_DIR, '..', 'config', 'testing.ini')


# -- Shared fixtures

@pytest.fixture(scope='session')
def dotenv() -> None:
    """Loads dotenv file
    """
    from aarau.env import Env

    # same as aarau:main
    dotenv_file = os.path.join(TEST_DIR, '..', '.env')
    Env.load_dotenv_vars(dotenv_file)
    return


@pytest.fixture(scope='session')
def env(dotenv) -> dict:
    """Returns env object
    """
    from aarau.env import Env

    return Env()


@pytest.fixture(scope='session')
def raw_settings(dotenv) -> dict:
    """Returns raw setting dict
    """
    from pyramid.paster import get_appsettings

    return get_appsettings('{0:s}#{1:s}'.format(INI_FILE, 'aarau'))


@pytest.fixture(scope='session')
def settings(raw_settings, resolve_settings) -> 'function':
    """Returns (environ) resolved settings
    """
    return resolve_settings(raw_settings)


@pytest.fixture(scope='session')
def resolve_settings() -> 'function':
    """Returns resolving function for settings
    """
    from aarau import resolve_settings

    def _resolve_settings(raw_s):
        return resolve_settings(raw_s)

    return _resolve_settings


@pytest.fixture(scope='session')
def extra_environ(env) -> dict:
    """Returns extra environ object
    """
    domain = env.get('DOMAIN', 'example.org')

    environ = {
        'HTTP_HOST': domain + ':80',
        'SERVER_NAME': domain,
        'SERVER_HOST': domain,
        'SERVER_PORT': '80',
        'REMOTE_ADDR': '127.0.0.1',
        'wsgi.url_scheme': 'http',
    }
    return environ


@pytest.fixture(scope='session')
def db(settings):
    """Returns initialized db instance
    """
    from aarau.models import DB, init_db

    return DB({
        'cardinal': init_db(settings, 'cardinal'),
        'analysis': init_db(settings, 'analysis'),
    })


@pytest.fixture(scope='function')
def get_mailer():
    """Returns getting mailer function
    """
    def _get_mailer(request_or_registry):
        from pyramid_mailer import get_mailer
        from zope.interface.interfaces import ComponentLookupError
        try:
            mailer = get_mailer(request_or_registry)
            return mailer
        except ComponentLookupError:
            pass

    return _get_mailer


# auto fixtures

@pytest.yield_fixture(autouse=True, scope='session')
def session_helper(db):
    """A helper function for session scope
    """
    db.cardinal.connect()
    db.analysis.connect()

    yield

    if not db.cardinal.is_closed():
        db.cardinal.close()

    if not db.analysis.is_closed():
        db.analysis.close()


@pytest.yield_fixture(autouse=True, scope='module')
def module_helper(settings, db):
    """A helper function for module scope
    """
    import sys

    from .data import import_data  # pylint: disable=import-error

    models = sys.modules['aarau.models']
    # pylint: disable=protected-access
    tables = [m.db_table for m in
              [getattr(models, k)._meta for k in models.__all__]
              if m.database != db['analysis']]

    # NOTE:
    # `db.create_tabels` and `ModelClass.create_table` will lost
    # custom enum fields...
    #
    #    db.create_tables(tables, safe=True)
    #    db.drop_tables(tables, safe=True)

    def truncate_tables(tables, cascade=False):
        """Truncates database tables
        """
        q = 'TRUNCATE table {0:s}'
        if cascade:
            q += ' CASCADE'

        for tbl in tables:
            db.cardinal.execute_sql(q.format(tbl))

    truncate_tables(tables, cascade=True)

    with db.cardinal.execution_context(with_transaction=True):
        import_data(settings)

    yield

    truncate_tables(tables, cascade=True)

    if not db.cardinal.is_closed():
        db.cardinal.close()


@pytest.yield_fixture(autouse=True, scope='function')
def function_helper(db):
    """A helper function for function scope
    """
    with db.cardinal.execution_context(with_transaction=True):
        yield

        if db.cardinal.is_closed():
            db.cardinal.connect()

        # to not bring any change into next test case
        db.cardinal.rollback()


# -- View tests

@pytest.fixture(scope='session')
def config(request, settings) -> Configurator:
    """Returns the testing config
    """
    from pyramid import testing

    config = testing.setUp(settings=settings)
    # FIXME:
    #    these includings from .ini file are not evaluated
    #    in unit tests.
    config.include('pyramid_assetviews')
    config.include('pyramid_beaker')
    config.include('pyramid_celery')
    config.include('pyramid_mako')
    config.include('pyramid_mailer.testing')
    config.include('pyramid_services')

    config.configure_celery(settings['__file__'])

    config.include('aarau.mailers')
    config.include('aarau.models')
    config.include('aarau.views')
    config.include('aarau.services')
    config.include('aarau.tasks')
    config.include('aarau.security')
    config.include('aarau.route')

    #config.add_translation_dirs('aarau:../locale')

    from pyramid.events import BeforeRender, NewRequest
    from aarau.utils import set_cache_controls
    from aarau.utils.template import add_template_util_renderer_globals
    from aarau.utils.localization import (
        add_localizer,
        add_localizer_renderer_globals,
    )
    from aarau.views.console import add_console_renderer_globals

    config.add_subscriber(set_cache_controls, BeforeRender)
    config.add_subscriber(add_localizer, NewRequest)
    config.add_subscriber(add_template_util_renderer_globals, BeforeRender)
    config.add_subscriber(add_localizer_renderer_globals, BeforeRender)
    config.add_subscriber(add_console_renderer_globals, BeforeRender)

    def teardown():
        """The teardown function
        """
        testing.tearDown()

    request.addfinalizer(teardown)

    return config


@pytest.fixture(scope='function')
def dummy_request(db, extra_environ) -> Request:
    """Returns Dummy request object
    """
    from pyramid import testing
    from pyramid_services import find_service
    from zope.interface.adapter import AdapterRegistry
    from aarau.utils.localization import get_translator_function

    locale_name = 'en'
    req = testing.DummyRequest(
        db=db,
        subdomain='',
        environ=extra_environ,
        _LOCALE_=locale_name,
        locale_name=locale_name,
        matched_route=None,
        settings={},
    )
    # for service objects
    req.service_cache = AdapterRegistry()
    req.find_service = (lambda *args, **kwargs:
                        find_service(req, *args, **kwargs))

    req.translate = get_translator_function(req.localizer)

    return req


@pytest.fixture(scope='function')
def projects():
    """Returns test projects
    """
    from aarau.models.project import Project

    return {p.namespace: p for p in Project.select()}


@pytest.fixture(scope='function')
def users():
    """Returns test users
    """
    from aarau.models.user import User

    return {u.username: u for u in User.select()}


@pytest.fixture(scope='function')
def publications():
    """Returns test publications
    """
    from aarau.models.publication import Publication

    return {p.name: p for p in Publication.select()}


@pytest.fixture(scope='function')
def articles():
    """Returns test articles
    """
    from aarau.models.article import Article

    return {a.slug: a for a in Article.select()}


@pytest.fixture(scope='function')
def plans():
    """Returns test plans
    """
    from aarau.models.plan import Plan

    return {p.name: p for p in Plan.select()}


@pytest.fixture(scope='function')
def mailer_outbox(dummy_request, get_mailer):
    """Returns dummy mailbox for out going emails
    """
    return get_mailer(dummy_request).outbox


# -- Functional tests

@pytest.fixture(scope='session')
def _app(raw_settings) -> Router:
    """Returns the internal app of app for testing
    """
    from aarau import main

    global_config = {
        '__file__': INI_FILE
    }
    if '__file__' in raw_settings:
        del raw_settings['__file__']

    return main(global_config, **raw_settings)


@pytest.fixture(scope='session')
def dummy_app(_app, extra_environ) -> TestApp:
    """Returns a dummy test app
    """
    return TestApp(_app, extra_environ=extra_environ)


@pytest.fixture(scope='function')
def mailbox(dummy_app, get_mailer):
    """Returns mailbox user interface for out going emails
    """
    # FIXME: mock `http` type.
    class Mailbox(object):
        """The Mailbox.
        """
        def __init__(self, request):
            # pylint: disable=too-many-function-args
            self._mailer = get_mailer(dummy_app.app.registry)

        @property
        def sent_messages(self):
            """Fetches sent messages from mailbox
            """
            # pylint: disable=no-member
            return self._mailer.outbox

        def clean(self):
            """Clears all messages in mailbox
            """
            # pylint: disable=no-member
            del self._mailer.outbox[:]

    return Mailbox(dummy_request)


@pytest.fixture(scope='function')
def login(dummy_app):
    """Login utility function
    """
    def _login(user, password=None):
        from os import path
        from aarau.yaml import yaml_loader

        users_yml = path.join(path.dirname(__file__), 'data', 'users.yml')
        with yaml_loader() as loader:
            data = loader(users_yml)
            user_passwords = {  # {'username': 'password'}
                d['username']: d['password'] for d in data['users']}

        if not password:
            password = user_passwords.get(user.username, None)

        res = dummy_app.get('/login', status=200)
        # TODO:
        #   See https://github.com/Pylons/webtest/issues/164
        #   To avoid warning for now. Remove `res.charset = None` in tests.
        res.charset = None
        token = res.html.select_one('input[name=csrf_token]')['value']
        params = {
            'csrf_token': token,
            'email': user.email,
            'password': password,
            'submit': '1',
        }
        res = dummy_app.post('/login', params, status=302)
        res.follow(status=200)
        return res

    return _login


@pytest.fixture(scope='function')
def logout(dummy_app):
    """Logout ulitity function
    """
    def _logout():
        res = dummy_app.get('/logout', status=302)
        res.follow(status=200)
        return res

    return _logout


@pytest.fixture(scope='function')
def login_as(login, logout):
    """Login utility for specified user
    """
    from contextlib import contextmanager

    @contextmanager
    def _login_as(user):
        login(user)
        try:
            yield
        finally:
            logout()
    return _login_as
