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
        rel_model=User, db_column='user_id', to_field='id',
        related_name='memberships', null=False)
    project = ForeignKeyField(
        rel_model=Project, db_column='project_id', to_field='id',
        related_name='memberships', null=True)
    role = EnumField(choices=roles, null=False, default='member')

    class Meta:
        db_table = 'memberships'

    def __repr__(self):
        return (
            '<Membership id:{} user_id:{} project_id:{} role:{}>'
        ).format(self.id, self.user_id, self.project_id, self.role)
