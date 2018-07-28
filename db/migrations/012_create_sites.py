# pylint: disable=C,R
from datetime import datetime

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase, EnumField


class Project(CardinalBase):
    class Meta:
        table_name = 'projects'


class Site(CardinalBase):
    calculation_states = ('off', 'on')

    id = PrimaryKeyField()
    project = ForeignKeyField(
        model=Project, column_name='project_id', field='id',
        backref='projects', null=False, index=True)
    hosting_id = IntegerField(null=True)
    hosting_type = CharField(max_length=32, null=True)
    domain = CharField(max_length=32, null=False)
    calculation_state = EnumField(
        choices=calculation_states,
        null=False, index=True, default='off')
    read_key = CharField(max_length=128, null=False, unique=True, index=True)
    write_key = CharField(max_length=128, null=False, unique=True, index=True)
    is_pinned = BooleanField(null=False, default=False)

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    deleted_at = DateTimeField(null=True)

    class Meta:
        table_name = 'sites'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Site)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Site, cascade=True)
