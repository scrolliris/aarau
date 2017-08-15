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

from aarau.models.base import Base, EnumField


class Project(Base):
    class Meta:
        db_table = 'projects'


class Site(Base):
    calculation_states = ('off', 'on')

    id = PrimaryKeyField()
    project = ForeignKeyField(
        rel_model=Project, db_column='project_id', to_field='id',
        related_name='projects', null=False, index=True)
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
        db_table = 'sites'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Site)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Site, cascade=True)
