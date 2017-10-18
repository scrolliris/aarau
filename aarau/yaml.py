import os
from ast import literal_eval
from datetime import datetime, timedelta
from contextlib import contextmanager
import importlib

from aarau.models import (  # noqa,pylint: disable=unused-import
    Project, Plan,
    Site,
    Publication, Article, Classification, License, Contribution,
    Application, Page,
    User, UserEmail,
)


@contextmanager
def tokenize(attributes):
    tokens = {}
    if not isinstance(attributes, dict):
        yield (tokens, attributes)

    for k in attributes.keys():
        if 'token' in k and callable(attributes[k]):
            tokens[k] = attributes[k]
            attributes[k] = '!token'

    yield (tokens, attributes)


@contextmanager
def set_password(fixture, attributes):
    if 'password' in attributes.keys():
        fixture.set_password(attributes['password'])
    yield fixture


def tag_token_user_email_activation(secret):
    def _tag_token_for_user_email_activation(_loader, node):
        def generate_token(user):
            return user.generate_token('user_email',
                                       secret=secret,
                                       salt='user_email_activation',
                                       expiration=literal_eval(node.value))
        return generate_token
    return _tag_token_for_user_email_activation


def tag_datetime_utcnow_plus_timedelta(_loader, node):
    return datetime.utcnow() + timedelta(seconds=literal_eval(node.value))


BY_NAMES = [
    ('user', 'username'),
    ('plan', 'name'),
    ('license', 'identifier'),
    ('project', 'namespace'),
    ('publication', 'name'),
    ('application', 'name'),
    ('classification', 'notation'),
    ('article', 'slug'),
]


def ref_functions():
    """Foreign key reference lookup function generator (xxx_id column).

    E.g. `!user.username "'john'"`
    """
    def import_by_name(module_name, klass_name):
        module = importlib.import_module(module_name)
        return getattr(module, klass_name)

    def _ref_function_factory(k, a):
        klass, field = import_by_name('aarau.models', k.title()), a

        def f():
            def _f(_loader, node):
                value = literal_eval(node.value)
                if not isinstance(value, str):
                    raise ValueError
                return klass.select().where(
                    getattr(klass, field) == value).get()

            return _f
        return f

    for k, a in BY_NAMES:
        name = '!{0:s}.{1:s}'.format(k, a)
        yield (name, _ref_function_factory(k, a))


@contextmanager
def yaml_loader(settings=None):
    import yaml

    def load_yaml(yml_file):
        data = {}
        if os.path.isfile(yml_file):
            with open(yml_file, 'r') as f:
                try:
                    data = yaml.load(f)
                except yaml.YAMLError as e:
                    print(e)
        return data

    # simple utility functions for tag in yaml
    if settings and isinstance(settings, dict):
        yaml.add_constructor(
            '!token.user_email_activation',
            tag_token_user_email_activation(settings['token.secret']))
        yaml.add_constructor(
            '!datetime.utcnow+timedelta',
            tag_datetime_utcnow_plus_timedelta)

        for tag, f in ref_functions():
            yaml.add_constructor(tag, f())

    yield load_yaml
