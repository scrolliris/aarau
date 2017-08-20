"""The license model.
"""
from peewee import (
    CharField,
    PrimaryKeyField,
)

from .base import CardinalBase, TimestampMixin


class License(CardinalBase, TimestampMixin):
    """License model class.
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    identifier = CharField(max_length=32, null=False, unique=True)
    fullname = CharField(max_length=64, null=False)
    url = CharField(max_length=128, null=False)

    class Meta:
        """The meta class of license.
        """
        # pylint: disable=too-few-public-methods
        db_table = 'licenses'

    def __repr__(self):
        return '<License id:{}, identifier:{}>'.format(
            self.id, self.identifier)

    @classmethod
    def get_by_identifier(cls, identifier):
        """Get a license by identifier string.
        """
        return cls.select().where(
            cls.identifier == identifier).get()
