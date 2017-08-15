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


class Article(Base):
    class Meta:
        db_table = 'articles'


class Contribution(Base):
    roles = ('primary_author', 'author', 'proofreader', 'cooperator',
             'translator', 'translation_supervisor', 'compiler', 'supervisor')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        rel_model=User, db_column='user_id', to_field='id',
        related_name='contributions', null=False, index=True)
    article = ForeignKeyField(
        rel_model=Article, db_column='article_id', to_field='id',
        related_name='contributions', null=False, index=True)
    role = EnumField(choices=roles, null=False, default='primary_author')

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        db_table = 'contributions'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Contribution)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Contribution, cascade=True)
