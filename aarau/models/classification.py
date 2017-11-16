from types import GeneratorType

from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    TimestampMixin,
    classproperty,
)


class Classification(CardinalBase, TimestampMixin):
    id = PrimaryKeyField()
    parent = ForeignKeyField(
        rel_model='self', db_column='parent_id', to_field='id',
        related_name='children', null=True)
    notation = CharField(max_length=64, null=False)
    name = CharField(max_length=128, null=False)

    class Meta:
        db_table = 'classifications'

    def __repr__(self):
        return '<Classification id:{} notation:{} name: {}>'.format(
            self.id, self.notation, self.name)

    @classproperty
    def as_choices(cls) -> GeneratorType:  # pylint: disable=no-self-argument
        """Returns classifications as choices."""
        return ((str(p.id), p.name) for p in cls.select(
            cls.id, cls.name).order_by(cls.id.asc()))
