# pylint: disable=C,R
from peewee import ForeignKeyField

from aarau.models.base import CardinalBase


class Chapter(CardinalBase):
    class Meta:
        table_name = 'chapters'


def migrate(migrator, _database, **_kwargs):
    migrator.add_fields(
        'articles',
        chapter_id=ForeignKeyField(
            model=Chapter, column_name='chapter_id', field='id',
            backref='articles', null=True, index=True)
    )


def rollback(migrator, _database, **_kwargs):
    migrator.remove_fields('articles', *[
        'chapter_id',
    ], cascade=True)
