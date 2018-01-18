from collections.abc import Mapping

import pytest

from webob.multidict import MultiDict, NestedMultiDict, NoVars
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.models import Site


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


# -- GET site_new (application)

def test_application_site_new_get_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_new(dummy_request)


def test_application_site_new_get(users, dummy_request):
    from aarau.views.console.site.form import build_new_application_site_form
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.POST = NoVars()
    project = user.projects[0]
    dummy_request.matchdict = {
        'namespace': project.namespace,
    }

    res = site_new(dummy_request)
    form = build_new_application_site_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


# -- POST site_new (application)

def test_application_site_new_post_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    query_param = {'type': 'application'}
    submit_body = {
        'submit': 'Create',
        # rest is omitted
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'namespace': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_new(dummy_request)


def test_application_site_new_post_with_validation_error(users, dummy_request):
    from aarau.views.console.site.form import build_new_application_site_form
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    project = user.projects[0]
    query_param = {'type': 'application'}
    submit_body = {
        'submit': 'Create',
        'csrf_token': dummy_request.session.get_csrf_token(),
        # invalid values
        'domain': '',
        'slug': '',
        'application-name': '',
        'application-description': '',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'namespace': project.namespace,
    }

    res = site_new(dummy_request)
    form = build_new_application_site_form(dummy_request)

    assert dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


def test_application_site_new_post(mocker, users, dummy_request):
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    project = user.projects[0]
    query_param = {'type': 'application'}
    submit_body = {
        'submit': 'Create',
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': 'new.example.org',
        'slug': 'new-example-org',
        'application-name': 'New Test Application',
        'application-description': '...',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'namespace': project.namespace
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

    assert 1 == len(project.applications)

    res = site_new(dummy_request)

    assert dummy_request.session.peek_flash('success')
    assert isinstance(res, HTTPFound)

    project.refresh()
    applications = project.applications
    assert 2 == len(applications)
    assert 1 == len(list(filter(lambda s: s.application.name ==
                                'New Test Application', applications)))

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.replicate.call_count


# -- GET site_overview (application)

# -- GET site_insights (application)

def test_application_site_insights_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_insights

    user = users['oswald']
    project = user.projects[0]
    site = project.applications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': '',  # invalid
        'slug': site.slug,
    }

    with pytest.raises(HTTPNotFound):
        site_insights(dummy_request)


def test_application_site_insights_missing_site(users, dummy_request):
    from aarau.views.console.site.action import site_insights

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    project = user.projects[0]
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_insights(dummy_request)


def test_application_site_insights(users, dummy_request):
    from aarau.views.console.site.action import site_insights

    user = users['oswald']
    project = user.projects[0]
    site = project.applications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': site.slug,
    }

    res = site_insights(dummy_request)

    assert isinstance(res, Mapping)
    assert ('instance', 'project', 'site') == tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['instance']


# -- GET site_settings_badges (application)

def test_application_site_settings_badges_missing_project(
        users, dummy_request):
    from aarau.views.console.site.action import site_settings_badges

    user = users['oswald']
    project = user.projects[0]
    site = project.applications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application'
    })
    dummy_request.matchdict = {
        'namespace': '',  # invalid
        'slug': site.slug,
    }

    with pytest.raises(HTTPNotFound):
        site_settings_badges(dummy_request)


def test_application_site_settings_badges_missing_site(users, dummy_request):
    from aarau.views.console.site.action import site_settings_badges

    user = users['oswald']
    project = user.projects[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': 0,  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_settings_badges(dummy_request)


def test_application_site_settings_badges(users, dummy_request):
    from aarau.views.console.site.action import site_settings_badges

    user = users['oswald']
    project = user.projects[0]
    site = project.applications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': site.slug,
    }
    res = site_settings_badges(dummy_request)

    assert isinstance(res, Mapping)
    assert ('instance', 'project', 'site') == tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['instance']


# -- GET site_settings_scripts (application)

def test_application_site_settings_scripts_missing_project(
        mocker, users, dummy_request):
    from aarau.views.console.site.action import site_settings_scripts

    user = users['oswald']
    project = user.projects[0]
    site = project.applications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': '',  # invalid
        'slug': site.slug,
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
        site_settings_scripts(dummy_request)

    # pylint: disable=no-member
    assert 0 == dummy_service.assign.call_count
    assert 0 == dummy_service.validate.call_count


def test_application_site_settings_scripts_missing_site(
        mocker, users, dummy_request):
    from aarau.views.console.site.action import site_settings_scripts

    user = users['oswald']
    project = user.projects[0]
    dummy_request.console = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': '',  # invalid
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
        site_settings_scripts(dummy_request)

    # pylint: disable=no-member
    assert 0 == dummy_service.assign.call_count
    assert 0 == dummy_service.validate.call_count


def test_application_site_settings_scripts(mocker, users, dummy_request):
    from aarau.views.console.site.action import site_settings_scripts

    user = users['oswald']
    project = user.projects[0]
    site = project.applications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'application',
    })
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': site.slug,
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

    res = site_settings_scripts(dummy_request)

    assert isinstance(res, Mapping)
    assert ('instance', 'project', 'replication_state', 'site') == \
        tuple(sorted(res.keys()))
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['instance']
    assert res['replication_state']

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.validate.call_count
