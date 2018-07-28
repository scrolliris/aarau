from datetime import datetime, timedelta

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField, TimestampMixin, TokenizerMixin
)
from aarau.models.user import User


class UserEmail(CardinalBase, TokenizerMixin, TimestampMixin):
    """Emails belong to a user.

    A user has multiple emails. User object has primary email.
    """

    activation_states = ('pending', 'active')
    types = ('primary', 'normal')

    id = PrimaryKeyField()
    user = ForeignKeyField(
        model=User, column_name='user_id', field='id',
        backref='emails', null=False)
    email = CharField(max_length=64, null=False, unique=True)
    type = EnumField(
        choices=types, null=False, default='normal')

    activation_state = EnumField(
        choices=activation_states, null=False, default='pending')
    activation_token = CharField(max_length=255, null=True)
    activation_token_expires_at = DateTimeField(
        null=True, default=None)

    def generate_activation_token(self, expiration=3600):
        token = self.generate_token(key='user_email',
                                    salt='user_email_activation',
                                    expiration=expiration)
        # TODO: Move email activation service
        self.activation_token = token
        self.activation_state = 'pending'
        self.activation_token_expires_at = datetime.utcnow() + \
            timedelta(seconds=expiration)
        return token

    def activate(self, token):
        data = self.decode_token(token, salt='user_email_activation')
        if data.get('user_email') != self.id:
            return False
        self.activation_state = 'active'
        self.activation_token = None
        self.activation_token_expires_at = None
        return self.save()

    def make_as_primary(self):
        klass = self.__class__
        with self._meta.database.atomic():
            try:
                current_primary = klass.select().where(
                    klass.user_id == self.user_id,
                    klass.activation_state == 'active',
                    klass.type == 'primary').get()
                current_primary.type = 'normal'
            except klass.DoesNotExist:
                self._meta.database.rollback()
                return False
            self.type = 'primary'
            self.user.email = self.email
            current_primary.save()
            return self.save()

    class Meta:
        table_name = 'user_emails'

    def __repr__(self):
        return '<UserEmail id:{}, user_id:{}, email:{}, activation_state:{}>' \
            .format(self.id, self.user_id, self.email, self.activation_state)
