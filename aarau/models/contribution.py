from peewee import (
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField, TimestampMixin
)

from aarau.models.article import Article
from aarau.models.user import User


class Contribution(CardinalBase, TimestampMixin):
    """Relationship between user and article."""

    roles = ('primary_author', 'author', 'proofreader', 'cooperator',
             'translator', 'translator_supervisor', 'compiler', 'supervisor')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        model=User, column_name='user_id', field='id',
        backref='contributions', null=False)
    article = ForeignKeyField(
        model=Article, column_name='article_id', field='id',
        backref='contributions', null=False)
    role = EnumField(choices=roles, null=False, default='primary_author')

    class Meta:
        table_name = 'contributions'

    def __repr__(self):
        return (
            '<Contribution id:{} article_id:{} user_id:{} role:{}>'
        ).format(self.id, self.article_id, self.user_id, self.role)
