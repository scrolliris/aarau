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
        rel_model=User, db_column='user_id', to_field='id',
        related_name='contributions', null=False)
    article = ForeignKeyField(
        rel_model=Article, db_column='article_id', to_field='id',
        related_name='contributions', null=False)
    role = EnumField(choices=roles, null=False, default='primary_author')

    class Meta:
        db_table = 'contributions'

    def __repr__(self):
        return (
            '<Contribution id:{} article_id:{} user_id:{} role:{}>'
        ).format(self.id, self.article_id, self.user_id, self.role)
