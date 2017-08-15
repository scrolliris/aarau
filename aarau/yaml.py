import os
from ast import literal_eval
from datetime import datetime, timedelta
from contextlib import contextmanager

from aarau.models import (  # noqa
    Project, Membership, Plan,
    Site,
    Publication, Article, Classification, License, Contribution,
    Application, Page,
    User, UserEmail,
)


@contextmanager
def tokenize(attributes={}):
    tokens = {}
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
    def _tag_token_for_user_email_activation(loader, node):
        def generate_token(user):
            return user.generate_token('user_email',
                                       secret=secret,
                                       salt='user_email_activation',
                                       expiration=literal_eval(node.value))
        return generate_token
    return _tag_token_for_user_email_activation


def tag_datetime_utcnow_plus_timedelta(loader, node):
    return datetime.utcnow() + timedelta(seconds=literal_eval(node.value))


by_names = [
    ('user', 'username'),
    ('plan', 'name'),
    ('license', 'identifier'),
    ('project', 'namespace'),
    ('publication', 'name'),
    ('application', 'name'),
    ('classification', 'notation'),
    ('article', 'slug'),
]

# functions to reference lookup relation (xxx_id column)
# e.g. `!user.username "'john'"`
ref_functions = {}
for m, f in by_names:
    def _ref_function_factory(m, f):
        klass = m.title()
        Klass, field = eval(klass), f

        def f():
            def _f(loader, node):
                value = literal_eval(node.value)
                if type(value) != str:
                    raise ValueError
                expr = eval("{0:s}.{1:s} == '{2:s}'".format(
                    klass, field, value))
                return Klass.select().where(expr).get()

            return _f
        return f

    name = '!{0:s}.{1:s}'.format(m, f)
    ref_functions[name] = _ref_function_factory(m, f)


@contextmanager
def yaml_loader(settings={}):
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
    if settings:
        yaml.add_constructor(
            '!token.user_email_activation',
            tag_token_user_email_activation(settings['token.secret']))
        yaml.add_constructor(
            '!datetime.utcnow+timedelta',
            tag_datetime_utcnow_plus_timedelta)

        for tag, f in ref_functions.items():
            yaml.add_constructor(tag, f())

    yield load_yaml
