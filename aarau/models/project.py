from peewee import (
    PrimaryKeyField,
    CharField,
    ForeignKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField,
    DeletedAtMixin,
    KeyMixin,
    TimestampMixin,
)

from aarau.models.plan import Plan
from aarau.models.application import Application
from aarau.models.publication import Publication


# pylint: disable=too-many-ancestors
class Project(CardinalBase, TimestampMixin, DeletedAtMixin, KeyMixin):
    """Publishing project as workspace."""

    billing_states = ('none', 'pending', 'processing', 'valid')

    id = PrimaryKeyField()
    access_key_id = CharField(max_length=128, null=False)
    plan = ForeignKeyField(
        model=Plan, column_name='plan_id', field='id',
        backref='publications', null=False)
    subscription_id = CharField(max_length=64, null=True)
    namespace = CharField(max_length=32, null=False)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    billing_state = EnumField(
        choices=billing_states, null=False, default='none')

    class Meta:
        table_name = 'projects'

    def __init__(self, *args, **kwargs):
        from peewee import ManyToManyField
        # avoid circular dependencies
        from .membership import Membership
        from .user import User

        users = ManyToManyField(
            model=User, backref='projects', through_model=Membership)
        self._meta.add_field('users', users)

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Project id:{} namespace:{} name:{} >'.format(
            self.id, self.namespace, self.name)

    @classmethod
    def get_by_access_key_id(cls, access_key_id):
        """Fetches a project by unique access_key_id string."""
        # pylint: disable=no-member
        return cls.select().where(
            cls.access_key_id_key == access_key_id,
            cls.billing_state == 'none' or cls.billing_state == 'valid').get()

    @property
    def applications(self):
        from .site import Site
        # pylint: disable=no-member
        return Site.select().join(Application, on=(
            (Site.instance_type == 'Application') &
            (Site.instance_id == Application.id))).where(
                Site.project_id == self.id)

    @property
    def publications(self):
        from .site import Site
        # pylint: disable=no-member
        return Site.select().join(Publication, on=(
            (Site.instance_type == 'Publication') &
            (Site.instance_id == Publication.id))).where(
                Site.project_id == self.id)

    @property
    def primary_owner(self):
        """Returns user as primary owner of this project.

        This may raise MembeshipDoesNotExist Exception.
        """
        from .membership import Membership
        from .user import User

        # pylint: disable=no-member
        m = (Membership
             .select(Membership, self.__class__, User)
             .join(User)
             .switch(Membership)
             .join(self.__class__)
             .where(
                 (Membership.role == 'primary_owner') &
                 (Membership.project_id == self.id)
             ).get())
        return m.user
