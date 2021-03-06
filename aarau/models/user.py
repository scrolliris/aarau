from datetime import datetime, timedelta

import bcrypt
from peewee import (
    CharField,
    DateTimeField,
    PrimaryKeyField,
)

from aarau.models.base import (
    CardinalBase,
    EnumField,
    TimestampMixin,
    TokenizerMixin,
)


# pylint: disable=too-many-ancestors
class User(CardinalBase, TokenizerMixin, TimestampMixin):
    """User account has a primary email for authentication."""

    activation_states = ('pending', 'active')

    id = PrimaryKeyField()
    name = CharField(max_length=64, null=True)
    username = CharField(max_length=32, null=True)
    email = CharField(max_length=64, null=False, unique=True)
    password = CharField(max_length=255, null=False)
    activation_state = EnumField(
        choices=activation_states, null=True, default='pending')

    reset_password_token = CharField(max_length=255, null=True)
    reset_password_token_expires_at = DateTimeField(
        null=True, default=None)
    reset_password_token_sent_at = DateTimeField(
        null=True, default=None)

    class Meta:
        table_name = 'users'

    @classmethod
    def encrypt_password(cls, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        return pwhash.decode('utf8')

    def __init__(self, *args, **kwargs):
        from peewee import ManyToManyField
        # pylint: disable=cyclic-import
        from .article import Article
        from .contribution import Contribution
        from .project import Project
        from .membership import Membership
        # pylint: enable=cyclic-import

        # collaborator
        projects = ManyToManyField(
            model=Project, backref='users', through_model=Membership)
        self._meta.add_field('projects', projects)

        # contributor
        articles = ManyToManyField(
            Article, backref='users', through_model=Contribution)
        self._meta.add_field('articles', articles)

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id:{}, email:{}>'.format(self.id, self.email)

    # TODO: Create custom field:
    # See: https://github.com/coleifer/peewee/blob/\
    #   dc0ac68f3a596e27e117698393b4ab64d2f92617/playhouse/fields.py#L54
    def set_password(self, pw):
        self.password = self.__class__.encrypt_password(pw)

    def verify_password(self, pw):
        if self.password is not None:
            expected_hash = self.password.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    def generate_reset_password_token(self, expiration=3600):
        token = self.generate_token(key='user',
                                    salt='reset_password',
                                    expiration=expiration)
        # TODO: Move reset password service
        self.reset_password_token = token
        self.reset_password_token_expires_at = datetime.utcnow() + \
            timedelta(seconds=expiration)
        return token

    def reset_password(self, token, password):
        data = self.decode_token(token, salt='reset_password')
        if data.get('user') != self.id:
            return False
        self.set_password(password)
        self.reset_password_token = None
        self.reset_password_token_expires_at = None
        self.reset_password_token_sent_at = None
        return self.save()
