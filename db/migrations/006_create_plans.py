# pylint: disable=C,R
from datetime import datetime

from peewee import (
    CharField,
    FloatField,
    DateTimeField,
    PrimaryKeyField,
    SmallIntegerField,
)

from aarau.models.base import CardinalBase


class Plan(CardinalBase):
    id = PrimaryKeyField()
    payment_type_id = SmallIntegerField(null=False, index=True)
    name = CharField(max_length=32, null=False)
    price = FloatField(null=False, default=0.00)
    description = CharField(max_length=64, null=False)

    created_at = DateTimeField(null=True, default=datetime.utcnow)
    updated_at = DateTimeField(null=True, default=datetime.utcnow)

    class Meta:
        table_name = 'plans'


def migrate(migrator, _database, **_kwargs):
    migrator.create_model(Plan)


def rollback(migrator, _database, **_kwargs):
    migrator.remove_model(Plan, cascade=True)
