# pylint: disable=C,R
from datetime import datetime

from peewee import (
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import Base, EnumField


class User(Base):
    class Meta:
        db_table = 'users'


class Project(Base):
    class Meta:
        db_table = 'projects'


class Membership(Base):
    roles = ('primary_owner', 'owner', 'member')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        rel_model=User, db_column='user_id', to_field='id',
        related_name='memberships', null=False, index=True)
    project = ForeignKeyField(
        rel_model=Project, db_column='project_id', to_field='id',
        related_name='memberships', null=True, index=True)
    role = EnumField(choices=roles, null=False, default='member')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        db_table = 'memberships'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Membership)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Membership, cascade=True)
