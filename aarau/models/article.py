from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
    PrimaryKeyField,
)
from playhouse.signals import pre_save

from aarau.models.base import (
    CardinalBase,
    EnumField,
    CodeMixin,
    DeletedAtMixin,
    TimestampMixin,
    classproperty,
)

from aarau.models.license import License
from aarau.models.publication import Publication


# pylint: disable=too-many-ancestors
class Article(CardinalBase, TimestampMixin, DeletedAtMixin, CodeMixin):
    scopes = ('public', 'private')
    progress_states = (
        'draft', 'wip', 'ready', 'scheduled', 'published',
        'rejected', 'archived')

    id = PrimaryKeyField()
    path = CharField(max_length=255, null=False)

    publication = ForeignKeyField(
        rel_model=Publication, db_column='publication_id', to_field='id',
        related_name='articles', null=False)
    code = CharField(max_length=128, null=False)
    title = CharField(max_length=255, null=True)
    scope = EnumField(choices=scopes, null=False, default='public')

    content = TextField(null=True)
    content_html = TextField(null=True)
    content_updated_at = DateTimeField(null=True)

    license = ForeignKeyField(
        rel_model=License, db_column='license_id', to_field='id',
        related_name='articles', null=True)
    copyright = CharField(max_length=64, null=False)
    progress_state = EnumField(
        choices=progress_states, null=False, default='draft')
    published_at = DateTimeField(null=True)

    class Meta:
        db_table = 'articles'

    def __init__(self, *args, **kwargs):
        from playhouse.fields import ManyToManyField
        # pylint: disable=cyclic-import
        from .contribution import Contribution
        from .user import User
        # pylint: enable=cyclic-import

        field = ManyToManyField(
            rel_model=User, related_name='users',
            through_model=Contribution)
        field.add_to_class(self.__class__, 'users')

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return (
            '<Article id:{} publication_id:{} progress_state:{} path:{}>'
        ).format(
            self.id, self.publication_id, self.progress_state, self.path)

    @classproperty
    def progress_state_as_choices(cls):
        """Returns choice pair as list for progress_state.

        See classproperty implementation.
        """
        # pylint: disable=no-self-argument
        return [(s, s) for s in cls.progress_states]

    @classmethod
    def published_on(cls, publication):
        """Provides scope by publication."""
        # pylint: disable=no-member
        return Article.select().join(Publication).where(
            Publication.id == publication.id)


@pre_save(sender=Article)
def on_save_handler(sender, instance, created):
    """Evaluated before save as hook.

    Updates published_at property, appropriately.
    """
    # pylint: disable=unused-argument
    # release
    if instance.progress_state == 'published' and not instance.published_at:
        instance.published_at = datetime.utcnow()
