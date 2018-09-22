# pylint: disable=C,R
from peewee import (
    ForeignKeyField,
    SmallIntegerField,
)

from aarau.models.base import CardinalBase


class Classification(CardinalBase):
    class Meta:
        table_name = 'classifications'


class ClassificationHierarchy(CardinalBase):
    ancestor = ForeignKeyField(
        model=Classification, column_name='ancestor_id', field='id',
        backref='descendants', null=False)
    descendant = ForeignKeyField(
        model=Classification, column_name='descendant_id', field='id',
        backref='ancestors', null=False)
    generations = SmallIntegerField(null=False)

    class Meta:
        primary_key = None
        auto_increment = False
        table_name = 'classification_hierarchies'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(ClassificationHierarchy)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(ClassificationHierarchy, cascade=True)
