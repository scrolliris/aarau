"""The classification model
"""
from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from .base import (
    CardinalBase,
    TimestampMixin,
)


class Classification(CardinalBase, TimestampMixin):
    """Classification identifier
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    parent = ForeignKeyField(
        rel_model='self', db_column='parent_id', to_field='id',
        related_name='children', null=True)
    notation = CharField(max_length=64, null=False)
    name = CharField(max_length=128, null=False)

    class Meta:  # pylint: disable=missing-docstring
        db_table = 'classifications'

    def __repr__(self):
        return '<Classification id:{} notation:{} name: {}>'.format(
            self.id, self.notation, self.name)
