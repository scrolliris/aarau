from pyramid.decorator import reify
from peewee import (
    BooleanField,
    CharField,
    IntegerField,
    ForeignKeyField,
    PrimaryKeyField,
    DeferredRelation,
)

from aarau.models.base import (
    CardinalBase,
    EnumField,
    DeletedAtMixin,
    KeyMixin,
    TimestampMixin,
)

from aarau.models.application import Application
from aarau.models.publication import Publication

DeferredProject = DeferredRelation()  # pylint: disable=invalid-name


# pylint: disable=too-many-ancestors
class Site(CardinalBase, TimestampMixin, DeletedAtMixin, KeyMixin):
    """Site model (website) belongs to a project.

    Site has its type as application (external site) or publication.
    """

    calculation_states = ('off', 'on')

    id = PrimaryKeyField()
    project = ForeignKeyField(
        rel_model=DeferredProject, db_column='project_id', to_field='id',
        related_name='sites', null=False, index=True)
    hosting_id = IntegerField(null=True)
    hosting_type = CharField(max_length=32, null=True)
    domain = CharField(max_length=32, null=True)
    slug = CharField(max_length=255, null=True)
    calculation_state = EnumField(
        choices=calculation_states,
        null=False, default='off')
    read_key = CharField(max_length=128, null=False)
    write_key = CharField(max_length=128, null=False)
    is_pinned = BooleanField(default=False)

    class Meta:
        db_table = 'sites'

    def __repr__(self):
        return '<Site id:{} project_id:{} domain:{} slug:{}>'.format(
            self.id, self.project_id, self.domain, self.slug)

    @reify
    def application(self):
        if self.hosting_type != 'Application':
            return None
        return Application.get(Application.id == self.hosting_id)

    @reify
    def publication(self):
        if self.hosting_type != 'Publication':
            return None
        return Publication.get(Publication.id == self.hosting_id)

    @classmethod
    def by_type(cls, type_name):
        if type_name not in ('application', 'publication'):
            return cls.select()
        hosting_type = type_name.capitalize()
        type_class = globals()[hosting_type]

        return cls.select(cls, type_class).join(type_class, on=(
            (cls.hosting_type == hosting_type) &
            (cls.hosting_id == type_class.id)))
