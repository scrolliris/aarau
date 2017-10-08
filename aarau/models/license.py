"""The license model
"""
from peewee import (
    CharField,
    PrimaryKeyField,
)

from .base import CardinalBase, TimestampMixin


class License(CardinalBase, TimestampMixin):
    """Open or proprietry license identifier
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    identifier = CharField(max_length=32, null=False, unique=True)
    fullname = CharField(max_length=64, null=False)
    url = CharField(max_length=128, null=False)

    class Meta:  # pylint: disable=missing-docstring
        db_table = 'licenses'

    def __repr__(self):
        return '<License id:{}, identifier:{}>'.format(
            self.id, self.identifier)

    @classmethod
    def get_by_identifier(cls, identifier):
        """Fetches a license by identifier string
        """
        return cls.select().where(
            cls.identifier == identifier).get()
