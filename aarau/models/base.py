from datetime import datetime
import hashlib
import re
import uuid

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from peewee import Field, SQL, DateTimeField
from playhouse.signals import Model, pre_save, pre_delete
from psycopg2.extras import NumericRange
from pyramid.decorator import reify

from aarau.models import db


class EnumField(Field):
    """Custom field as Enum."""

    def __ddl_type_name(self):
        # e.g. e_user_activation_state
        model_name = re.sub(
            '([A-Z])', '_\\1', self.model.__name__).lower()
        return 'e{}_{}'.format(model_name, self.name)

    # https://www.postgresql.org/docs/9.5/static/datatype-enum.html
    def pre_field_create(self, model):
        """A hook before field creation."""
        field_type = self.__ddl_type_name()

        _db = model._meta.database  # pylint: disable=protected-access
        q = 'DROP TYPE IF EXISTS {0:s} CASCADE;'.format(field_type)
        _db.execute_sql(q)

        tail = ', '.join(["'{}'"] * len(self.choices)).format(
            *self.choices)
        q = 'CREATE TYPE {0:s} AS ENUM ({1:s});'.format(field_type, tail)
        _db.execute_sql(q)

    def post_field_create(self, _model):
        """A hook after field creation."""
        pass

    # https://github.com/coleifer/peewee/blob/\
    #     dc0ac68f3a596e27e117698393b4ab64d2f92617/peewee.py#L888
    #
    # from peewee 3, coerce has been renamed to adapt.
    def adapt(self, value):
        """Validates as valid choice & sanitize as string."""
        if value not in self.choices:
            raise Exception("Invalid Enum value `%s`" % value)
        return str(value)

    def ddl_datatype(self, ctx):
        return SQL(self.__ddl_type_name())


class NumericRangeField(Field):
    # pylint: disable=no-self-use
    """Range type field definition for numeric value."""

    field_type = 'numrange'

    def db_value(self, value):
        """Returns value for database."""
        if isinstance(value, (list, tuple)) and len(value) == 2:
            return NumericRange(lower=float(value[0]), upper=float(value[1]),
                                bounds='[]', empty=False)
        return value

    def python_value(self, value):
        return value


class CardinalBase(Model):
    """Main base model class."""

    class Meta:
        database = db.cardinal

    @classmethod
    def create_table(cls, safe=True, **options):
        """Creates database table for class itself."""
        # pylint: disable=no-member
        for field in cls._meta.sorted_fields:
            if hasattr(field, 'pre_field_create'):
                field.pre_field_create(cls)
        super().create_table(safe, **options)
        for field in cls._meta.sorted_fields:
            if hasattr(field, 'post_field_create'):
                field.post_field_create(cls)

    def refresh(self):
        """Refetches object attributes from database."""
        newer_self = type(self).get(self._pk_expr())
        for field_name in self._meta.fields.keys():
            val = getattr(newer_self, field_name)
            setattr(self, field_name, val)
            self._dirty.clear()
        return newer_self


class AnalysisBase(Model):
    """Analysis base model class."""

    class Meta:
        database = db.analysis


class TimestampMixin(Model):
    """Mixin for timestamp fields."""

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)


@pre_save(sender=TimestampMixin)
def before_save_timestamp_mixin(_model_class, instance, **options):
    # pylint: disable=unused-argument
    """A hook before save for model mixed TimestampMixin."""
    instance.updated_at = datetime.utcnow()


class DeletedAtMixin(Model):
    """Mixin adding a deleted_at field."""

    deleted_at = DateTimeField(null=True)

    def delete_instance(self, *args, **kwargs):
        # TODO: Nullify columns :'(
        return self.save(*args, **kwargs)


@pre_delete(sender=DeletedAtMixin)
def before_delete_deleted_at_mixin(_model_class, instance):
    # pylint: disable=unused-argument
    """A hook before delete for model mixed DeletedAtMixin."""
    instance.deleted_at = datetime.utcnow()


class TokenizerMixin(object):
    """Mixin for token fiels and utilities."""

    @reify
    def _settings(self):  # pylint: disable=no-self-use
        from aarau import get_settings
        return get_settings()

    def generate_token(self, key, secret=None, salt='token', expiration=3600):
        """Generates new token with secret and salt."""
        if not secret:
            secret = self._settings['token.secret']

        s = Serializer(secret, expiration, salt=salt)
        return s.dumps({key: self.id}).decode('utf8')

    def decode_token(self, token, secret=None, salt='token'):
        """Extracts data in token as decode."""
        if not secret:
            secret = self._settings['token.secret']

        s = Serializer(secret, salt=salt)
        try:
            data = s.loads(token)
            return data
        except (TypeError, BadSignature, SignatureExpired):
            return {}


class CodeMixin(object):
    """Mixin has utility methods to treat code field."""

    @classmethod
    def generate_code(cls):
        """Generates hashed UUID4 with SHA1 as code."""
        m = hashlib.sha1()
        m.update(uuid.uuid4().bytes)
        return m.hexdigest()

    @classmethod
    def grab_unique_code(cls):
        """Returns generated new code after check it isn't in db."""
        code = None
        while True:
            code = cls.generate_code()
            try:
                cls.get(cls.code == code)
            except cls.DoesNotExist:
                break
        return code


class KeyMixin(object):
    """Mixin has has key fields which are generated with UUID."""

    @classmethod
    def generate_key(cls):
        """Generates hashed UUID4 with SHA1 as key."""
        m = hashlib.sha1()
        m.update(uuid.uuid4().bytes)
        return m.hexdigest()

    @classmethod
    def grab_unique_key(cls, field):
        """Returns generated new key after check it isn't in db."""
        key = None
        while True:
            key = cls.generate_key()
            try:
                cls.get(getattr(cls, field) == key)
            except cls.DoesNotExist:
                break
        return key


class ClassProperty:
    """Decorator as classproperty.

    Use like `@classproperty`
    """

    def __init__(self, f):
        self._f = f

    def __get__(self, _, owner):
        return self._f(owner)


# pylint: disable=invalid-name
classproperty = ClassProperty
