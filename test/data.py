import os
import re

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
                    if fixture.is_dirty:
                        fixture.save()

                    for k, f in tokens.items():
                        setattr(fixture, k, f(fixture))
                        fixture.save()

        # tests/data/*.yml
        fixtures = [
            Plan, Classification, License, Project, Publication,
            Chapter, Article, Application, Page, Site, User, UserEmail,
            Membership, Contribution,
        ]

        for model in fixtures:
            # pylint: disable=no-member,protected-access
            table = model._meta.table_name
            fixtures_dir = os.path.join(os.path.dirname(__file__), 'data')
            files = [f for f in os.listdir(fixtures_dir) if
                     f.startswith(table) and f.endswith('.yml')]

            # e.g. classification.yml, classification.1.yml...
            for f in sorted(files, key=(lambda v: int(
                    re.sub(r'[a-z\_]', '', v).replace('.', '0')))):
                fixture_yml = os.path.join(fixtures_dir, f)
                if os.path.isfile(fixture_yml):
                    data = loader(fixture_yml)
                    for attributes in data[table]:
                        blend_data(model, attributes)
