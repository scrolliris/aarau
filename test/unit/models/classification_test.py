import pytest

from peewee import fn
from aarau.models import Classification, ClassificationHierarchy


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_as_choices_as_classproperty():
    from types import GeneratorType

    choices = Classification.as_choices
    assert isinstance(choices, GeneratorType)

    # TODO: only roots
    expected_names = [
        'Science and Knowledge. Organization. Computer Science. Information. '
        'Documentation. Librarianship. Institutions. Publications',
        'Philosophy. Psychology',
        'Religion. Theology',
        'Social sciences',
        'Vacant',
        'Mathematics. Natural sciences',
        'Applied sciences. Medicine. Technology',
        'The arts. Recreation. Entertainment. Sport',
        'Language. Linguistics. Literature',
        'Geography. Biography. History',
    ]
    # pylint: disable=not-an-iterable
    assert expected_names == [n for _, n in choices]


def test_roots():
    assert 10 == len(Classification.roots)


def test_rebuild_all():
    # pylint: disable=no-value-for-parameter
    assert 0 == ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)).scalar()

    Classification.rebuild_all()

    # NOTE: no children
    assert 10 == ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)).scalar()


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

    c = Classification.get()
    c.rebuild()

    assert 1 == ClassificationHierarchy.select(
        fn.COUNT(ClassificationHierarchy.ancestor)).scalar()
