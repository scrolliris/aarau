"""The Contribution model.
"""
from peewee import (
    ForeignKeyField,
    PrimaryKeyField,
)

from .base import Base, EnumField, TimestampMixin

from .article import Article
from .user import User


class Contribution(TimestampMixin, Base):
    """Contribution model class.
    """
    # pylint: disable=too-few-public-methods
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
        """The meta class of Contribution.
        """
        db_table = 'contributions'

    def __repr__(self):
        return (
            '<Contribution id:{} article_id:{} user_id:{} role:{}>'
        ).format(self.id, self.article_id, self.user_id, self.role)
