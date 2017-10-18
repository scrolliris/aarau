from os import path

from mixer.backend.peewee import Mixer

from aarau.yaml import (
    yaml_loader,
    tokenize,
    set_password
)

# pylint:disable=unused-wildcard-import,wildcard-import
from aarau.models import *


def import_data(settings):
    mixer = Mixer()

    with yaml_loader(settings) as loader:
        def blend_data(klass, attributes):
            with tokenize(attributes) as (tokens, attrs):

                fixture = mixer.blend(klass, **attrs)
                fixture.save()

                with set_password(fixture, attrs) as fixture:
                    fixture.save()

                    for k, f in tokens.items():
                        setattr(fixture, k, f(fixture))
                        fixture.save()

        # tests/data/*.yml
        data_fixtures = [
            ('plans', Plan),
            ('classifications', Classification),
            ('licenses', License),
            ('projects', Project),
            ('publications', Publication),
            ('articles', Article),
            ('applications', Application),
            ('pages', Page),
            ('sites', Site),
            ('users', User),
            ('user_emails', UserEmail),
            ('memberships', Membership),
            ('contributions', Contribution),
        ]
        for table, klass in data_fixtures:
            yml_file = path.join(path.dirname(__file__), 'data',
                                 '{0:s}.yml'.format(table))
            data = loader(yml_file)

            for attributes in data[table]:
                blend_data(klass, attributes)
