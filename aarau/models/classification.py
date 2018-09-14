from types import GeneratorType

from peewee import (
    CharField,
    ForeignKeyField,
    PrimaryKeyField,
)

from aarau.utils.sql import format_sql
from aarau.models.base import (
    CardinalBase,
    TimestampMixin,
    classproperty,
)


class Classification(CardinalBase, TimestampMixin):
    id = PrimaryKeyField()
    parent = ForeignKeyField(
        model='self', column_name='parent_id', field='id',
        backref='children', null=True)
    notation = CharField(max_length=64, null=False)
    name = CharField(max_length=128, null=False)

    class Meta:
        table_name = 'classifications'

    def __repr__(self):
        return '<Classification id:{} notation:{} name: {}>'.format(
            self.id, self.notation, self.name)

    @classproperty
    def as_choices(cls) -> GeneratorType:  # pylint: disable=no-self-argument
        """Returns classifications as choices."""
        # TODO: (for now) roots only
        return ((str(p.id), p.name) for p in
                cls.select(cls.id, cls.name)
                .where(cls.parent_id >> None).order_by(cls.notation.asc()))

    @classproperty
    def roots(cls):  # pylint: disable=no-self-argument
        return cls.select().where(cls.parent_id >> None)

    @classmethod
    def rebuild_all(cls) -> None:
        from aarau.models.classification_hierarchy import \
            ClassificationHierarchy

        # pylint: disable=protected-access
        q = 'TRUNCATE table {0:s} CASCADE'.format(
            ClassificationHierarchy._meta.table_name)
        ClassificationHierarchy._meta.database.execute_sql(q)

        for root in cls.roots:  # pylint: disable=not-an-iterable
            root.rebuild()

    @property
    def is_root(self) -> bool:
        return self.parent_id is None

    def rebuild(self) -> None:  # pylint: disable=function-redefined
        # pylint: disable=protected-access
        """Rebuilds hierarchies recursively."""
        from aarau.models.classification_hierarchy import \
            ClassificationHierarchy

        # delete hierarchy
        q = '''
DELETE FROM {table_name:s}
WHERE descendant_id IN (
  SELECT DISTINCT descendant_id
  FROM (
    SELECT descendant_id FROM {table_name:s}
    WHERE ancestor_id = %s OR descendant_id = %s
  ) AS h
)
'''
        q = format_sql(q).format(
            table_name=ClassificationHierarchy._meta.table_name)
        ClassificationHierarchy._meta.database.execute_sql(
            q, params=(self.id, self.id,))

        # new
        ClassificationHierarchy.create(
            ancestor=self, descendant=self, generations=0)

        if not self.is_root:
            q = '''
INSERT INTO {table_name:s} (ancestor_id, descendant_id, generations)
 SELECT h.ancestor_id, %s, h.generations + 1
 FROM {table_name:s} h
 WHERE h.descendant_id = %s
'''
            q = format_sql(q).format(
                table_name=ClassificationHierarchy._meta.table_name)

            ClassificationHierarchy._meta.database.execute_sql(
                q, params=(self.id, self.parent_id,))

        for child in self.children:
            child.rebuild()
