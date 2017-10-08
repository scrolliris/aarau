"""The project model.
"""
from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from .base import (
    CardinalBase,
    EnumField,
    DeletedAtMixin,
    KeyMixin,
    TimestampMixin,
)

from .plan import Plan
from .site import Site
from .application import Application
from .publication import Publication


class Project(CardinalBase, TimestampMixin, DeletedAtMixin, KeyMixin):
    """Publishing project as workspace
    """
    # pylint: disable=too-many-ancestors
    billing_states = ('none', 'pending', 'processing', 'valid')

    id = PrimaryKeyField()
    access_key_id = CharField(max_length=128, null=False)
    plan = ForeignKeyField(
        rel_model=Plan, db_column='plan_id', to_field='id',
        related_name='publications', null=False)
    subscription_id = CharField(max_length=64, null=True)
    namespace = CharField(max_length=32, null=False)
    name = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=True)
    billing_state = EnumField(
        choices=billing_states, null=False, default='none')

    class Meta:  # pylint: disable=missing-docstring
        db_table = 'projects'

    def __init__(self, *args, **kwargs):
        from playhouse.fields import ManyToManyField
        # avoid circular dependencies
        from .membership import Membership
        from .user import User

        field = ManyToManyField(
            rel_model=User, related_name='users',
            through_model=Membership)
        field.add_to_class(self.__class__, 'users')

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Project id:{} namespace:{} name:{} >'.format(
            self.id, self.namespace, self.name)

    @classmethod
    def get_by_access_key_id(cls, access_key_id):
        """Fetches a project by unique access_key_id string
        """
        # pylint: disable=no-member
        return cls.select().where(
            cls.access_key_id_key == access_key_id,
            cls.billing_state == 'none' or cls.billing_state == 'valid').get()

    @property
    def application_sites(self):
        """Fetches external application sites
        """
        # pylint: disable=no-member
        return Site.select().join(Application, on=(
            (Site.hosting_type == 'Application') &
            (Site.hosting_id == Application.id))).where(
                Site.project_id == self.id)

    @property
    def publication_sites(self):
        """Returns internal publication sites
        """
        # pylint: disable=no-member
        return Site.select().join(Publication, on=(
            (Site.hosting_type == 'Publication') &
            (Site.hosting_id == Publication.id))).where(
                Site.project_id == self.id)

    @property
    def primary_owner(self):
        """Returns user as primary owner of this project
        """
        from .membership import Membership
        from .user import User

        return self.users.select(User, Membership).where(
            Membership.role == 'primary_owner').get()
