import pytest

from aarau.views.console.site.application.action import (
    application_site_new,
    application_site_view_badge,
    application_site_view_result,
    application_site_view_script,
)

from aarau.models import Site


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_application_site_new_get_missing_project(users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

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
    from webob.multidict import NestedMultiDict, NoVars
    from aarau.views.console.site.form import build_new_application_site_form

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

    assert isinstance(res, dict)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


def test_application_site_new_post_missing_project(users, dummy_request):
    from webob.multidict import MultiDict, NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    query = {'type': 'application'}
    data = {
        'submit': 'Create',
        # rest is omitted
    }
    dummy_request.GET = NestedMultiDict(query)
    dummy_request.POST = MultiDict(data)
    dummy_request.params = NestedMultiDict({**query, **data})
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
    }

    with pytest.raises(HTTPNotFound):
        application_site_new(dummy_request)


def test_application_site_new_post_with_validation_error(users, dummy_request):
    from webob.multidict import MultiDict, NestedMultiDict
    from aarau.views.console.site.form import build_new_application_site_form

    user = users['oswald']
    project = user.projects[0]
    dummy_request.user = user
    query = {'type': 'application'}
    data = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        # invalid values
        'domain': '',
        'application-name': '',
        'application-description': '',
        'submit': 'Create',
    }
    dummy_request.GET = NestedMultiDict(query)
    dummy_request.POST = MultiDict(data)
    dummy_request.params = NestedMultiDict({**query, **data})
    dummy_request.matchdict = {
        'project_id': project.id
    }

    res = application_site_new(dummy_request)
    form = build_new_application_site_form(dummy_request)

    assert dummy_request.session.peek_flash('failure')
    assert isinstance(res, dict)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


def test_application_site_new_post(mocker, users, dummy_request):
    from pyramid.httpexceptions import HTTPFound
    from webob.multidict import MultiDict, NestedMultiDict

    user = users['oswald']
    project = user.projects[0]
    dummy_request.user = user
    query = {'type': 'application'}
    data = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': 'new.example.org',
        'application-name': 'New Test Application',
        'application-description': '...',
        'submit': 'Create',
    }
    dummy_request.GET = NestedMultiDict(query)
    dummy_request.POST = MultiDict(data)
    dummy_request.params = NestedMultiDict({**query, **data})
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


def test_application_site_badge_missing_project(users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application'
    })
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
        'id': site.id,
    }

    with pytest.raises(HTTPNotFound):
        application_site_view_badge(dummy_request)


def test_application_site_badge_missing_site(users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

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
        application_site_view_badge(dummy_request)


def test_application_site_badge(users, dummy_request):
    from webob.multidict import NestedMultiDict

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

    assert isinstance(res, dict)
    assert ('application', 'project', 'site') == tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']


def test_application_site_result_missing_project(users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
        'id': site.id,
    }

    with pytest.raises(HTTPNotFound):
        application_site_view_result(dummy_request)


def test_application_site_result_missing_site(users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

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


def test_application_site_result(users, dummy_request):
    from webob.multidict import NestedMultiDict

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

    assert isinstance(res, dict)
    assert ('application', 'project', 'site') == tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']


def test_application_site_script_missing_project(mocker, users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    project = user.projects[0]
    site = project.application_sites[0]
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


def test_application_site_script_missing_site(mocker, users, dummy_request):
    from webob.multidict import NestedMultiDict
    from pyramid.httpexceptions import HTTPNotFound

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


def test_application_site_script(mocker, users, dummy_request):
    from webob.multidict import NestedMultiDict

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

    assert isinstance(res, dict)
    assert ('application', 'project', 'replication_state', 'site') == \
        tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']
    assert res['replication_state']

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.validate.call_count
