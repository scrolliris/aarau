import pytest

from aarau.models import Classification


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_as_choices_as_classproperty():
    from types import GeneratorType

    choices = Classification.as_choices
    assert isinstance(choices, GeneratorType)

    expected_names = [
        'Philosophy. Psychology',
        'Religion. Theology',
        'Science and Knowledge. Organization. Computer Science. Information. '
        'Documentation. Librarianship. Institutions. Publications',
    ]
    # pylint: disable=not-an-iterable
    assert expected_names == sorted([n for _, n in choices])
