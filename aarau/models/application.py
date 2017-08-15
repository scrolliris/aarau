"""The application model.
"""
from peewee import (
    CharField,
    PrimaryKeyField,
)

from .base import (
    Base,
    DeletedAtMixin,
    TimestampMixin,
)


class Application(TimestampMixin, DeletedAtMixin, Base):
    """Application model class.
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)

    class Meta:
        """The meta class of application.
        """
        # pylint: disable=too-few-public-methods
        db_table = 'applications'

    def __repr__(self):
        return '<Application id:{} name:{}>'.format(self.id, self.name)
