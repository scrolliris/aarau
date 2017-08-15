"""The page model.
"""
from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from .base import (
    Base,
    EnumField,
    CodeMixin,
    DeletedAtMixin,
    TimestampMixin,
)

from .application import Application


class Page(TimestampMixin, DeletedAtMixin, CodeMixin, Base):
    """Page model class.
    """
    # pylint: disable=too-many-ancestors
    scopes = ('public', 'private')

    id = PrimaryKeyField()
    application = ForeignKeyField(
        rel_model=Application, db_column='application_id', to_field='id',
        related_name='pages', null=False)
    code = CharField(max_length=128, null=True)
    path = CharField(max_length=255, null=False)
    title = CharField(max_length=128, null=True)
    scope = EnumField(choices=scopes, null=False, default='public')

    class Meta:
        """The meta class of page.
        """
        # pylint: disable=too-few-public-methods
        db_table = 'pages'

    def __repr__(self):
        return '<Page id:{} application_id:{} title:{}>'.format(
            self.id, self.application_id, self.title)
