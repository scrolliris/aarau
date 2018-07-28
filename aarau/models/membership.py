from peewee import (
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField, TimestampMixin
)

from aarau.models.user import User
from aarau.models.project import Project


# pylint: disable=too-many-ancestors
class Membership(CardinalBase, TimestampMixin):
    """Relationship between user and project."""

    roles = ('primary_owner', 'owner', 'member')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        model=User, column_name='user_id', field='id',
        backref='memberships', null=False)
    project = ForeignKeyField(
        model=Project, column_name='project_id', field='id',
        backref='memberships', null=True)
    role = EnumField(choices=roles, null=False, default='member')

    class Meta:
        table_name = 'memberships'

    def __repr__(self):
        return (
            '<Membership id:{} user_id:{} project_id:{} role:{}>'
        ).format(self.id, self.user_id, self.project_id, self.role)
