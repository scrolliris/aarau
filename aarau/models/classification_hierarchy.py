from peewee import (
    ForeignKeyField,
    SmallIntegerField,
)

from aarau.models.base import CardinalBase
from aarau.models.classification import Classification


class ClassificationHierarchy(CardinalBase):
    ancestor = ForeignKeyField(
        model=Classification, column_name='ancestor_id', field='id',
        backref='descendant_hierarchies', null=False)
    descendant = ForeignKeyField(
        model=Classification, column_name='descendant_id', field='id',
        backref='ancestor_hierarchies', null=False)
    generations = SmallIntegerField(null=False)

    class Meta:
        table_name = 'classification_hierarchies'

    def __repr__(self):
        return '''\
<ClassificationHierarchy ancestor_id:{} descendant_id:{} generations: {}>\
'''.format(self.ancestor_id, self.descendant_id, self.generations)
