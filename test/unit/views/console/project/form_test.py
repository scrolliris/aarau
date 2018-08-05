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
    from aarau.views import form
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


@pytest.mark.parametrize('namespace', [
    'abc',  # too short
    '-abcde',  # invalid char position `-`
    '001-project',  # non-alphabet at start
    'scrolliris',  # reserved
    'loooong-namespace',  # too long
])
def test_namespace_validations_with_invalid_inputs(namespace, dummy_request):
    project = Project(namespace=namespace)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': 'project-name',
        'namespace': namespace,
    })
    form = build_project_form(dummy_request, project)
    assert not form.validate()


@pytest.mark.parametrize('namespace', [
    'abcdef',
    'lorem-ipsum',
    'project-01',
    'one-project-two',
    'looong-namespace',
])
def test_namespace_validations_with_valid_inputs(namespace, dummy_request):
    project = Project(namespace=namespace)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': 'project-name',
        'namespace': namespace,
    })
    form = build_project_form(dummy_request, project)
    assert form.validate()
    assert not form.namespace.errors
