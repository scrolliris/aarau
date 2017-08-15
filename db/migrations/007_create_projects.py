# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import Base, EnumField


class Plan(Base):
    class Meta:
        db_table = 'plans'


class Project(Base):
    billing_states = ('none', 'pending', 'processing', 'valid')

    id = PrimaryKeyField()
    access_key_id = CharField(
        max_length=128, null=False, unique=True, index=True)
    plan = ForeignKeyField(
        rel_model=Plan, db_column='plan_id', to_field='id',
        related_name='projects', null=False, index=True)
    subscription_id = CharField(max_length=64, null=True, index=True)
    namespace = CharField(max_length=32, null=False)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    billing_state = EnumField(
        choices=billing_states, null=False, default='none')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)
    deleted_at = DateTimeField(null=True)

    class Meta:
        db_table = 'projects'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Project)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Project, cascade=True)
