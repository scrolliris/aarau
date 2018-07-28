from peewee import (
    PrimaryKeyField,
    CharField,
)

from aarau.models.base import (
    CardinalBase,
    DeletedAtMixin,
    TimestampMixin,
)


class Application(CardinalBase, TimestampMixin, DeletedAtMixin):
    """User's external site application."""

    id = PrimaryKeyField()
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)

    class Meta:
        table_name = 'applications'

    def __repr__(self):
        return '<Application id:{} name:{}>'.format(self.id, self.name)
