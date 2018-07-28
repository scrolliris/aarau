from peewee import (
    PrimaryKeyField,
    CharField,
    ForeignKeyField,
)

from aarau.models.base import (
    CardinalBase,
    DeletedAtMixin,
    TimestampMixin,
)

from aarau.models.license import License
from aarau.models.classification import Classification


class Publication(CardinalBase, TimestampMixin, DeletedAtMixin):
    """Internal publication which published on scrolliris."""

    id = PrimaryKeyField()
    classification = ForeignKeyField(
        model=Classification, column_name='classification_id', field='id',
        backref='publications', null=False)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    license = ForeignKeyField(
        model=License, column_name='license_id', field='id',
        backref='publications', null=True)
    copyright = CharField(max_length=64, null=False)

    class Meta:
        table_name = 'publications'

    def __repr__(self):
        return '<Publication id:{} name:{}>'.format(self.id, self.name)
