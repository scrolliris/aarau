""" Base class and extensions for model class
"""
from datetime import datetime
import hashlib
import re
import uuid

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from peewee import Field, SQL, DateTimeField
from playhouse.signals import Model, pre_save, pre_delete
from pyramid.decorator import reify

# pylint: disable=import-self
from . import db


class EnumField(Field):
    """ Custom field as Enum
    """
    db_field = 'enum'

    # https://www.postgresql.org/docs/9.5/static/datatype-enum.html
    def pre_field_create(self, model):
        """ A hook before field creation
        """
        field = self.__ddl__column_name__()

        _db = self.get_database()
        q = 'DROP TYPE IF EXISTS {0:s} CASCADE;'.format(field)
        _db.execute_sql(q)

        tail = ', '.join(["'{}'"] * len(self.choices)).format(
            *self.choices)
        q = 'CREATE TYPE {0:s} AS ENUM ({1:s});'.format(field, tail)
        _db.execute_sql(q)

    def post_field_create(self, model):
        """ A hook after field creation
        """
        self.db_field = self.__ddl__column_name__()

    # https://github.com/coleifer/peewee/blob/\
    #     dc0ac68f3a596e27e117698393b4ab64d2f92617/peewee.py#L888
    def coerce(self, value):
        """ Validate as valid choice & sanitize as string
        """
        if value not in self.choices:
            raise Exception("Invalid Enum value `%s`", value)
        return str(value)

    def get_column_type(self):
        """ Column type name
        """
        return 'enum'

    def __ddl__column_name__(self):
        # e.g. e_user_activation_state
        model_name = re.sub(
            '([A-Z])', '_\\1', self.model_class.__name__).lower()
        return 'e{}_{}'.format(model_name, self.name)

    def __ddl_column__(self, _ctype):
        return SQL(self.__ddl__column_name__())


class Base(Model):
    """ Base model class
    """
    class Meta:
        # pylint: disable=too-few-public-methods
        """ The meta class
        """
        database = db

    @classmethod
    def get_by_id(cls, model_id):
        """ Fetch objects via its id attribute
        """
        # pylint: disable=no-member
        return cls.get(cls.id == model_id)

    @classmethod
    def create_table(cls, *args, **kwargs):
        """ Create database table for class itself
        """
        # pylint: disable=no-member
        for field in cls._meta.declared_fields:
            if hasattr(field, 'pre_field_create'):
                field.pre_field_create(cls)
        super().create_table(*args, **kwargs)
        for field in cls._meta.declared_fields:
            if hasattr(field, 'post_field_create'):
                field.post_field_create(cls)

    def refresh(self):
        """ Refetch object attributes from database
        """
        newer_self = type(self).get(self._pk_expr())
        for field_name in self._meta.fields.keys():
            val = getattr(newer_self, field_name)
            setattr(self, field_name, val)
            self._dirty.clear()
        return newer_self


class TimestampMixin(Base):
    """ Adds timestamp fields as mixin
    """
    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)


@pre_save(sender=TimestampMixin)
def before_save_timestamp_mixin(model_class, instance, created):
    # pylint: disable=unused-argument
    """ A hook before save for model mixed TimestampMixin
    """
    instance.updated_at = datetime.utcnow()


class DeletedAtMixin(Base):
    """ Adds a deleted_at field as mixin
    """
    deleted_at = DateTimeField(null=True)

    def delete_instance(self, *args, **kwargs):
        # TODO: nullify columns :'(
        return self.save(*args, **kwargs)


@pre_delete(sender=DeletedAtMixin)
def before_delete_deleted_at_mixin(model_class, instance):
    # pylint: disable=unused-argument
    """ A hook before delete for model mixed DeletedAtMixin
    """
    instance.deleted_at = datetime.utcnow()


class TokenizerMixin(Base):
    """ Adds token fiels and utilities for model mixed TokenizerMixin
    """
    @reify
    def _settings(self):
        # pylint: disable=no-self-use
        from aarau import get_settings
        return get_settings()

    def generate_token(self, key, secret=None, salt='token', expiration=3600):
        """ Generates new token with secret and salt
        """
        if not secret:
            secret = self._settings['token.secret']

        s = Serializer(secret, expiration, salt=salt)
        return s.dumps({key: self.id}).decode('utf8')

    def decode_token(self, token, secret=None, salt='token'):
        """ Extract data in token as decode
        """
        if not secret:
            secret = self._settings['token.secret']

        s = Serializer(secret, salt=salt)
        try:
            data = s.loads(token)
            return data
        except Exception as e:
            # TODO: handle exception `itsdangerous.SignatureExpired`
            return {}


class CodeMixin(Base):
    """ Adds utility methods to treat code field for model mixed CodeMixin
    """
    @classmethod
    def generate_code(cls):
        """ Generates hashed UUID4 with SHA1 as code
        """
        m = hashlib.sha1()
        m.update(uuid.uuid4().bytes)
        return m.hexdigest()

    @classmethod
    def grab_unique_code(cls):
        """ Returns generated new code as attribute after check it isn't in db
        """
        code = None
        while True:
            code = cls.generate_code()
            try:
                cls.get(cls.code == code)
            except cls.DoesNotExist:
                break
        return code


class KeyMixin(Base):
    """The utility mixin to treat key fields for model.
    """
    @classmethod
    def generate_key(cls):
        """Generates hashed UUID4 with SHA1 as key
        """
        m = hashlib.sha1()
        m.update(uuid.uuid4().bytes)
        return m.hexdigest()

    @classmethod
    def grab_unique_key(cls, field):
        """Returns generated new key as attribute after check it isn't in db.
        """
        key = None
        while True:
            key = cls.generate_key()
            try:
                cls.get(getattr(cls, field) == key)
            except cls.DoesNotExist:
                break
        return key


class ClassProperty:
    # pylint: disable=too-few-public-methods
    """ The classproperty decorator

    Use like `@classproperty`
    """
    def __init__(self, f):
        self._f = f

    def __get__(self, _, owner):
        return self._f(owner)


# pylint: disable=invalid-name
classproperty = ClassProperty
