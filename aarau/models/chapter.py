from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    TimestampMixin,
)

from aarau.models.publication import Publication


class Chapter(CardinalBase, TimestampMixin):
    id = PrimaryKeyField()
    publication = ForeignKeyField(
        model=Publication, column_name='publication_id', field='id',
        backref='chapters', null=False, index=True)
    parent = ForeignKeyField(
        model='self', column_name='parent_id', field='id',
        backref='children', null=True, index=True)
    slug = CharField(max_length=255, null=False, unique=True, index=True)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)

    class Meta:
        table_name = 'chapters'

    def __repr__(self):
        return '<Chapter id:{} name:{}>'.format(self.id, self.name)
