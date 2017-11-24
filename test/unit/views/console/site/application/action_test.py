from collections.abc import Mapping

import pytest

from webob.multidict import MultiDict, NestedMultiDict, NoVars
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.models import Site


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


# GET application_site_new

def test_application_site_new_get_missing_project(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_new

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
    }

    with pytest.raises(HTTPNotFound):
        application_site_new(dummy_request)


def test_application_site_new_get(users, dummy_request):
    from aarau.views.console.site.form import build_new_application_site_form
    from aarau.views.console.site.application.action import \
        application_site_new

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.POST = NoVars()
    project = user.projects[0]
    dummy_request.matchdict = {
        'project_id': project.id,
    }

    res = application_site_new(dummy_request)
    form = build_new_application_site_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


# POST application_site_new

def test_application_site_new_post_missing_project(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_new

    user = users['oswald']
    query_param = {'type': 'application'}
    submit_body = {
        'submit': 'Create',
        # rest is omitted
    }
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
    }

    with pytest.raises(HTTPNotFound):
        application_site_new(dummy_request)


def test_application_site_new_post_with_validation_error(users, dummy_request):
    from aarau.views.console.site.form import build_new_application_site_form
    from aarau.views.console.site.application.action import \
        application_site_new

    user = users['oswald']
    project = user.projects[0]
    query_param = {'type': 'application'}
    submit_body = {
        'submit': 'Create',
        'csrf_token': dummy_request.session.get_csrf_token(),
        # invalid values
        'domain': '',
        'application-name': '',
        'application-description': '',
    }
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'project_id': project.id
    }

    res = application_site_new(dummy_request)
    form = build_new_application_site_form(dummy_request)

    assert dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


def test_application_site_new_post(mocker, users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_new

    user = users['oswald']
    project = user.projects[0]
    query_param = {'type': 'application'}
    submit_body = {
        'submit': 'Create',
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': 'new.example.org',
        'application-name': 'New Test Application',
        'application-description': '...',
    }
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'project_id': project.id
    }

    class DummyService(object):
        # pylint: disable=no-self-use
        def assign(self, *_args, **_kwargs):
            pass

        def replicate(self, *_args, **_kwargs):
            return True

    dummy_service = DummyService()
    mocker.spy(dummy_service, 'assign')
    mocker.spy(dummy_service, 'replicate')

    dummy_request.find_service = (lambda *args, **kwargs: dummy_service)

    assert 1 == len(project.application_sites)

    res = application_site_new(dummy_request)

    assert dummy_request.session.peek_flash('success')
    assert isinstance(res, HTTPFound)

    project.refresh()
    application_sites = project.application_sites
    assert 2 == len(application_sites)
    assert 1 == len(list(filter(lambda s: s.application.name ==
                                'New Test Application', application_sites)))

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.replicate.call_count


# GET application_site_view_badge

def test_application_site_view_badge_missing_project(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_badge

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application'
    })
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
        'id': site.id,
    }

    with pytest.raises(HTTPNotFound):
        application_site_view_badge(dummy_request)


def test_application_site_view_badge_missing_site(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_badge

    user = users['oswald']
    project = user.projects[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': 0,  # invalid
    }

    with pytest.raises(HTTPNotFound):
        application_site_view_badge(dummy_request)


def test_application_site_view_badge(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_badge

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': site.id,
    }
    res = application_site_view_badge(dummy_request)

    assert isinstance(res, Mapping)
    assert ('application', 'project', 'site') == tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']


# GET application_site_view_result

def test_application_site_view_result_missing_project(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_result

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
        'id': site.id,
    }

    with pytest.raises(HTTPNotFound):
        application_site_view_result(dummy_request)


def test_application_site_view_result_missing_site(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_result

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    project = user.projects[0]
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': 0,  # invalid
    }

    with pytest.raises(HTTPNotFound):
        application_site_view_result(dummy_request)


def test_application_site_view_result(users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_result

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': site.id,
    }

    res = application_site_view_result(dummy_request)

    assert isinstance(res, Mapping)
    assert ('application', 'project', 'site') == tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']


# GET application_site_view_script

def test_application_site_view_script_missing_project(
        mocker, users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_script

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
        'id': site.id,
    }

    class DummyService(object):
        # pylint: disable=no-self-use
        def assign(self, *_args, **_kwargs):
            pass

        def validate(self, *_args, **_kwargs):
            return True

    dummy_service = DummyService()
    mocker.spy(dummy_service, 'assign')
    mocker.spy(dummy_service, 'validate')

    dummy_request.find_service = (lambda *args, **kwargs: dummy_service)

    with pytest.raises(HTTPNotFound):
        application_site_view_script(dummy_request)

    # pylint: disable=no-member
    assert 0 == dummy_service.assign.call_count
    assert 0 == dummy_service.validate.call_count


def test_application_site_view_script_missing_site(
        mocker, users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_script

    user = users['oswald']
    project = user.projects[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': 0,  # invalid
    }

    class DummyService(object):
        # pylint: disable=no-self-use
        def assign(self, *_args, **_kwargs):
            pass

        def validate(self, *_args, **_kwargs):
            return True

    dummy_service = DummyService()
    mocker.spy(dummy_service, 'assign')
    mocker.spy(dummy_service, 'validate')

    dummy_request.find_service = (lambda *args, **kwargs: dummy_service)

    with pytest.raises(HTTPNotFound):
        application_site_view_script(dummy_request)

    # pylint: disable=no-member
    assert 0 == dummy_service.assign.call_count
    assert 0 == dummy_service.validate.call_count


def test_application_site_view_script(mocker, users, dummy_request):
    from aarau.views.console.site.application.action import \
        application_site_view_script

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': site.id,
    }

    class DummyService(object):
        # pylint: disable=no-self-use
        def assign(self, *_args, **_kwargs):
            pass

        def validate(self, *_args, **_kwargs):
            return True

    dummy_service = DummyService()
    mocker.spy(dummy_service, 'assign')
    mocker.spy(dummy_service, 'validate')

    dummy_request.find_service = (lambda *args, **kwargs: dummy_service)

    res = application_site_view_script(dummy_request)

    assert isinstance(res, Mapping)
    assert ('application', 'project', 'replication_state', 'site') == \
        tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']
    assert res['replication_state']

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.validate.call_count
