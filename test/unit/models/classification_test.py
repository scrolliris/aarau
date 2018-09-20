import pytest

from peewee import fn
from aarau.models import Classification, ClassificationHierarchy


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_roots():
    assert 10 == len(Classification.roots)


def test_rebuild_all():
    # pylint: disable=no-value-for-parameter
    assert 0 == ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)).scalar()

    Classification.rebuild_all()

    assert 0 != ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)).scalar()


def test_subtree_all():
    Classification.rebuild_all()

    # pylint: disable=no-value-for-parameter
    assert Classification.select(fn.COUNT(Classification.id)).scalar() == \
        len([c.id for c in Classification.subtree_all()])


def test_is_root():
    c = Classification.create(
        parent_id=None, notation='abc', name='dummy')
    assert c.is_root

    roots = Classification.roots
    # pylint: disable=unsubscriptable-object
    c = Classification.create(
        parent_id=roots[0], notation='abc', name='dummy')
    assert not c.is_root


def test_rebuild():
    # pylint: disable=no-value-for-parameter
    assert 0 == ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)).scalar()

    c = Classification.select().where(Classification.notation == '0').get()
    c.rebuild()

    assert 0 != ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)
    ).where(ClassificationHierarchy.ancestor_id == c.id).scalar()
