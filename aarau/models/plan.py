"""The plan model.
"""
from peewee import (
    CharField,
    FloatField,
    PrimaryKeyField,
    SmallIntegerField,
)

from .base import (
    CardinalBase,
    TimestampMixin,
    classproperty
)


class Plan(CardinalBase, TimestampMixin):
    """Plan model class.
    """
    # pylint: disable=too-many-ancestors
    id = PrimaryKeyField()
    payment_type_id = SmallIntegerField(null=False)
    name = CharField(max_length=32, null=False)
    price = FloatField(null=False, default=0.00)
    description = CharField(max_length=64, null=False)

    class Meta:
        """The meta class of plan.
        """
        # pylint: disable=too-few-public-methods
        db_table = 'plans'

    def __repr__(self):
        return '<Plan id:{}, name:{}>'.format(self.id, self.name)

    @classmethod
    def get_free_plan(cls):
        """Returns free plan.
        """
        return cls.select().where(cls.name == 'plan.free.name').get()

    @classproperty
    def as_choices(cls):  # pylint: disable=no-self-argument
        """Returns plans as choices.
        """
        return [(str(p.id), p.name) for p in cls.select(
            cls.id, cls.name).order_by(cls.id.asc())]
