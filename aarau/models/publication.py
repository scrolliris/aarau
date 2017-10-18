from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
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
        rel_model=Classification, db_column='classification_id', to_field='id',
        related_name='publications', null=False)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    license = ForeignKeyField(
        rel_model=License, db_column='license_id', to_field='id',
        related_name='publications', null=True)
    copyright = CharField(max_length=64, null=False)

    class Meta:
        db_table = 'publications'

    def __repr__(self):
        return '<Publication id:{} name:{}>'.format(self.id, self.name)
