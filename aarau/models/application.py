"""The application model
"""
from peewee import (
    CharField,
    PrimaryKeyField,
)

from .base import (
    CardinalBase,
    DeletedAtMixin,
    TimestampMixin,
)


class Application(CardinalBase, TimestampMixin, DeletedAtMixin):
    """User's external site
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)

    class Meta:  # pylint: disable=missing-docstring
        db_table = 'applications'

    def __repr__(self):
        return '<Application id:{} name:{}>'.format(self.id, self.name)
