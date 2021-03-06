from pyramid.decorator import reify
from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField,
    DeletedAtMixin,
    KeyMixin,
    TimestampMixin,
)

from aarau.models.project import Project
from aarau.models.application import Application
from aarau.models.publication import Publication


# pylint: disable=too-many-ancestors
class Site(CardinalBase, TimestampMixin, DeletedAtMixin, KeyMixin):
    """Site model (website) belongs to a project.

    Site has its type as application (external site) or publication.
    """

    calculation_states = ('off', 'on')
    instance_types = ('Application', 'Publication')

    id = PrimaryKeyField()
    slug = CharField(max_length=255, null=True)

    instance_id = IntegerField(null=True)
    instance_type = CharField(max_length=32, null=True)
    domain = CharField(max_length=64, null=True)
    calculation_state = EnumField(
        choices=calculation_states,
        null=False, default='off')
    read_key = CharField(max_length=128, null=False)
    write_key = CharField(max_length=128, null=False)
    is_pinned = BooleanField(default=False)

    project = ForeignKeyField(
        model=Project, column_name='project_id', field='id',
        backref='sites', null=False, index=True)

    class Meta:
        table_name = 'sites'

    def __repr__(self):
        return '<Site id:{} project_id:{} domain:{} slug:{}>'.format(
            self.id, self.project_id, self.domain, self.slug)

    @reify
    def type(self):
        """Lower case alias to instance_type attribute."""
        return str(self.instance_type).lower()

    @reify
    def instance(self):
        return getattr(self, self.type)

    def instantiate(self, *args, **kwargs):
        return globals()[self.instance_type](*args, **kwargs)

    @reify
    def application(self):
        if self.type != 'application' or not self.instance_id:
            return None
        return Application.get(Application.id == self.instance_id)

    @reify
    def publication(self):
        if self.type != 'publication' or not self.instance_id:
            return None
        return Publication.get(Publication.id == self.instance_id)
