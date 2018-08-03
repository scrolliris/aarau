import pytest
from webob.multidict import MultiDict
from wtforms import ValidationError

from aarau.models.project import Project
from aarau.views.console.project.form import (
    build_project_form,
    namespace_availability_check,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views.console.project import form

    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_namespace_availability_check(mocker, dummy_request):
    project = Project(namespace='scrolliris')

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_project_form(dummy_request, project)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=project.namespace)
        namespace_availability_check(form, field)
