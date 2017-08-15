"""The publication model.
"""
from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from .base import (
    Base,
    DeletedAtMixin,
    TimestampMixin,
)

from .license import License
from .classification import Classification


class Publication(TimestampMixin, DeletedAtMixin, Base):
    """Publication model class.
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    classification = ForeignKeyField(
        rel_model=Classification, db_column='classification_id', to_field='id',
        related_name='publications', null=False)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    license = ForeignKeyField(
        rel_model=License, db_column='license_id', to_field='id',
        related_name='publications', null=True)
    copyright = CharField(max_length=64, null=False)

    class Meta:
        """The meta class of publication.
        """
        # pylint: disable=too-few-public-methods
        db_table = 'publications'

    def __repr__(self):
        return '<Publication id:{} name:{}>'.format(self.id, self.name)
