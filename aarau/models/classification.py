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

    @classmethod
    def subtree_all(cls, limit_depth=None):
        return cls.get_subtree(limit_depth=limit_depth)

    @classmethod
    def get_subtree(cls, scope=None, limit_depth=None):
        from peewee import fn
        from .classification_hierarchy import ClassificationHierarchy

        having_clause = fn.MAX(ClassificationHierarchy.generations) <= \
            limit_depth - 1 if limit_depth is not None else None

        generation_depth = (ClassificationHierarchy.select(
            ClassificationHierarchy.descendant_id,
            fn.MAX(ClassificationHierarchy.generations).alias('depth')
        ).group_by(
            ClassificationHierarchy.descendant_id
        ).having(
            having_clause
        ).alias('generation_depth').order_by(
            ClassificationHierarchy.descendant_id.asc()))

        predicate = ((Classification.id == generation_depth.c.descendant_id))
        return (scope if scope else cls).select().join(
            generation_depth, on=predicate)

    @classmethod
    def find_by_notation(cls, notation):
        return cls.select().where(cls.notation == notation).get()

    @property
    def is_root(self) -> bool:
        return self.parent_id is None

    @property
    def ancestor_ids(self):
        from .classification_hierarchy import ClassificationHierarchy
        return [a.ancestor_id for a in
                self.ancestor_hierarchies.select().order_by(
                    ClassificationHierarchy.generations.asc())]

    @property
    def ancestors(self):
        return self.__class__.select().where(
            self.__class__.id << self.ancestor_ids)

    @property
    def descendant_ids(self):
        from .classification_hierarchy import ClassificationHierarchy
        return [a.descendant_id for a in
                self.descendant_hierarchies.select().order_by(
                    ClassificationHierarchy.generations.asc())]

    @property
    def descendants(self):
        """All descendants incl. itself. """
        return self.__class__.select().where(
            self.__class__.id << self.descendant_ids)

    def subtree(self, limit_depth=None):
        return self.__class__.get_subtree(
            scope=self.descendants, limit_depth=limit_depth)

    def rebuild(self) -> None:  # pylint: disable=function-redefined
        # pylint: disable=protected-access
        """Rebuilds hierarchies recursively."""
        from .classification_hierarchy import ClassificationHierarchy

        # delete its hierarchies
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
        # NOTE: `Model.create` will return "id" using returning clause even if
        # the  Model does not have primary key field. Then use `insert` here.
        ClassificationHierarchy.insert(
            ancestor=self, descendant=self,
            generations=0).returning(None).execute()

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
