from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField,
    CodeMixin,
    DeletedAtMixin,
    TimestampMixin,
)

from aarau.models.application import Application


# pylint: disable=too-many-ancestors
class Page(CardinalBase, TimestampMixin, DeletedAtMixin, CodeMixin):
    """Web page belong to user's application, which is recorded via script."""

    scopes = ('public', 'private')

    id = PrimaryKeyField()
    path = CharField(max_length=255, null=False)

    application = ForeignKeyField(
        model=Application, column_name='application_id', field='id',
        backref='pages', null=False)
    code = CharField(max_length=128, null=True)
    title = CharField(max_length=128, null=True)
    scope = EnumField(choices=scopes, null=False, default='public')

    class Meta:
        table_name = 'pages'

    def __repr__(self):
        return '<Page id:{} application_id:{} title:{}>'.format(
            self.id, self.application_id, self.title)
