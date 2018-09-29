from datetime import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
    TextField,
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
        model=Publication, column_name='publication_id', field='id',
        backref='articles', null=False)
    code = CharField(max_length=128, null=False)
    title = CharField(max_length=255, null=True)
    scope = EnumField(choices=scopes, null=False, default='public')

    content = TextField(null=True)
    content_html = TextField(null=True)
    content_updated_at = DateTimeField(null=True)

    license = ForeignKeyField(
        model=License, column_name='license_id', field='id',
        backref='articles', null=True)
    copyright = CharField(max_length=64, null=False)
    progress_state = EnumField(
        choices=progress_states, null=False, default='draft')
    published_at = DateTimeField(null=True)

    users = None

    class Meta:
        table_name = 'articles'

    def __init__(self, *args, **kwargs):
        from peewee import ManyToManyField
        # pylint: disable=cyclic-import
        from .contribution import Contribution
        from .user import User
        # pylint: enable=cyclic-import

        users = ManyToManyField(
            model=User, backref='articles', through_model=Contribution)
        self._meta.add_field('users', users)

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
        return [(str(i), v) for (i, v) in enumerate(cls.progress_states)]

    @classmethod
    def published_on(cls, publication):
        """Provides scope by publication."""
        # pylint: disable=no-member
        return Article.select().join(Publication).where(
            Publication.id == publication.id)

    @property
    def available_progress_states_as_choices(self) -> list:
        """Returns a list contains tulples hold indices and values."""
        # TODO: state machine?
        next_states = self.next_progress_states()
        return [  # pylint: disable=not-an-iterable
            (i, v) for (i, v) in self.__class__.progress_state_as_choices
            if self.progress_state == v or v in next_states
        ]

    def next_progress_states(self) -> tuple:
        """Returns state names for next based on current progress_state."""
        # pylint: disable=too-many-return-statements
        if self.progress_state == 'draft':
            return ('wip', 'ready', 'archived')
        if self.progress_state == 'wip':
            return ('draft', 'ready', 'archived')
        if self.progress_state == 'ready':
            return ('wip', 'scheduled', 'published', 'rejected', 'archived')
        if self.progress_state == 'scheduled':
            return ('ready', 'published', 'archived')
        if self.progress_state == 'published':
            return ('archived',)
        if self.progress_state == 'rejected':
            return ('wip', 'archived')
        if self.progress_state == 'archived':
            return ('draft', 'wip')
        return self.__class__.progress_states


@pre_save(sender=Article)
def on_save_handler(sender, instance, created):
    """Evaluated before save as hook.

    Updates published_at property, appropriately.
    """
    # pylint: disable=unused-argument
    # release
    if instance.progress_state == 'published' and not instance.published_at:
        instance.published_at = datetime.utcnow()
