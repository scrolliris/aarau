import os
from ast import literal_eval
from datetime import datetime, timedelta
from contextlib import contextmanager
import importlib

from aarau.models import (  # noqa,pylint: disable=unused-import
    Project, Plan,
    Site,
    Publication, Chapter, Article, Classification, License, Contribution,
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


TAGS = [
    ('user', 'username'),
    ('plan', 'name'),
    ('license', 'identifier'),
    ('project', 'namespace'),
    ('publication', 'name'),
    ('application', 'name'),
    ('classification', 'notation'),
    ('chapter', 'slug'),
    ('article', 'path'),
]


def build_constructors(tags):
    """Foreign key lookup constructors.

    E.g. `!user.username "'john'"`
    """
    def import_by_name(module_name, klass_name):
        module = importlib.import_module(module_name)
        return getattr(module, klass_name)

    def build_constructor(klass, field):
        def f(_loader, node):
            value = literal_eval(node.value)
            # ScalarNode
            if not isinstance(value, str):
                raise ValueError
            data = klass.select().where(
                getattr(klass, field) == value).get()
            yield data

        return f

    for k, a in tags:
        klass, field = import_by_name('aarau.models', k.title()), a
        tag = '!{0:s}.{1:s}'.format(k, a)

        yield (tag, build_constructor(klass, field))


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

        for tag, c in build_constructors(TAGS):
            yaml.add_constructor(tag, c)

    yield load_yaml
