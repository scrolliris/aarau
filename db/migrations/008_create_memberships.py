# pylint: disable=C,R
from datetime import datetime

from peewee import (
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import CardinalBase, EnumField


class User(CardinalBase):
    class Meta:
        table_name = 'users'


class Project(CardinalBase):
    class Meta:
        table_name = 'projects'


class Membership(CardinalBase):
    roles = ('primary_owner', 'owner', 'member')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        model=User, column_name='user_id', field='id',
        backref='memberships', null=False, index=True)
    project = ForeignKeyField(
        model=Project, column_name='project_id', field='id',
        backref='memberships', null=True, index=True)
    role = EnumField(choices=roles, null=False, default='member')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'memberships'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Membership)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Membership, cascade=True)
