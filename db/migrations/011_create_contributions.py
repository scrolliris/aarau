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


class Article(CardinalBase):
    class Meta:
        table_name = 'articles'


class Contribution(CardinalBase):
    roles = ('primary_author', 'author', 'proofreader', 'cooperator',
             'translator', 'translation_supervisor', 'compiler', 'supervisor')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        model=User, column_name='user_id', field='id',
        backref='contributions', null=False, index=True)
    article = ForeignKeyField(
        model=Article, column_name='article_id', field='id',
        backref='contributions', null=False, index=True)
    role = EnumField(choices=roles, null=False, default='primary_author')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'contributions'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Contribution)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Contribution, cascade=True)
