from collections.abc import Mapping

import pytest

from webob.multidict import (
    MultiDict,
    NestedMultiDict,
    NoVars,
)
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from aarau.models import Membership


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views import form
    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


# -- GET project_new


def test_project_new_get(users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.console.project.action import project_new

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = {}
    # this an assignment is needed to avoid error form building (must be empty)
    dummy_request.POST = NoVars()
    dummy_request.matchdict = {}

    res = project_new(dummy_request)
    form = build_new_project_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)


# -- POST project_new

def test_project_new_namespace_validation_error_with_missing_namespace(
        users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.console.project.action import project_new

    user = users['oswald']
    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': '',
        # invalid namespace
        'namespace': '',
        'description': '',
        'submit': 'Create',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {}

    res = project_new(dummy_request)
    form = build_new_project_form(dummy_request)

    assert ['project.creation.failure'] == \
        dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    f = res['form']
    assert ['This field is required.'] == f.namespace.errors


def test_project_new_namespace_validation_error_with_invalid_pattern(
        users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.console.project.action import project_new

    user = users['oswald']
    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': '',
        # invalid namespace
        'namespace': '-with-hyphen',
        'description': '',
        'submit': 'Create',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {}

    res = project_new(dummy_request)
    form = build_new_project_form(dummy_request)

    assert ['project.creation.failure'] == \
        dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    f = res['form']
    assert ['Invalid input.'] == f.namespace.errors


def test_project_new_namespace_validation_error_with_reserved_word(
        users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.console.project.action import project_new

    user = users['oswald']
    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': '',
        # invalid namespace in reserved_words.sample.yml
        'namespace': 'scrolliris',
        'description': '',
        'submit': 'Create',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {}

    res = project_new(dummy_request)
    form = build_new_project_form(dummy_request)

    assert ['project.creation.failure'] == \
        dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    f = res['form']
    assert ['Namespace is unavailable.'] == f.namespace.errors


def test_project_new(users, dummy_request):
    from aarau.views.console.project.action import project_new

    user = users['oswald']
    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': 'My New Project',
        'namespace': 'my-new-project',
        'description': 'This is my new project.',
        'submit': 'Create',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {}

    assert 1 == len(user.projects)

    res = project_new(dummy_request)

    assert ['project.creation.success'] == \
        dummy_request.session.peek_flash('success')
    assert isinstance(res, HTTPFound)
    assert '/projects/my-new-project' == res.location

    user.refresh()
    assert 2 == len(user.projects)
    assert 1 == len(list(filter(
        lambda p: p.namespace == 'my-new-project', user.projects)))


def test_project_settings_namespace_validation_error_with_missing_namespace(
        users, dummy_request):
    from aarau.views.console.project.form import build_edit_project_form
    from aarau.views.console.project.action import project_settings

    user = users['oswald']
    project = user.projects[0]

    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': project.name,
        'namespace': '',  # invalid namespace
        'description': project.description,
        'submit': 'Update',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {'namespace': project.namespace}

    res = project_settings(dummy_request)
    form = build_edit_project_form(dummy_request, project)

    assert ['project.update.failure'] == \
        dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form', 'project') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    f = res['form']
    assert ['This field is required.'] == f.namespace.errors


def test_project_settings_invalid_namespace_in_matchdict(users, dummy_request):
    from aarau.views.console.project.action import project_settings

    user = users['oswald']
    project = user.projects[0]

    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': 'Updated Project Name',
        'namespace': project.namespace,
        'description': project.description,
        'submit': 'Update',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})

    # other project
    invalid_project = list(
        users['weenie'].projects.where(Membership.role == 'primary_owner'))[0]
    dummy_request.matchdict = {'namespace': invalid_project.namespace}

    assert 1 == len(user.projects)

    with pytest.raises(HTTPNotFound):
        project_settings(dummy_request)

    assert [] == dummy_request.session.peek_flash('failure')
    assert [] == dummy_request.session.peek_flash('success')


def test_project_settings(users, dummy_request):
    from aarau.views.console.project.action import project_settings

    user = users['oswald']
    project = user.projects[0]

    query_param = {}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': 'Updated Project Name',
        'namespace': project.namespace,
        'description': project.description,
        'submit': 'Update',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {'namespace': project.namespace}

    assert 1 == len(user.projects)

    res = project_settings(dummy_request)

    assert ['project.update.success'] == \
        dummy_request.session.peek_flash('success')
    assert isinstance(res, HTTPFound)
    assert '/projects/{:s}/settings'.format(project.namespace) == res.location

    user.refresh()
    assert 1 == len(user.projects)
    assert 1 == len(list(filter(
        lambda p: p.namespace == project.namespace, user.projects)))
