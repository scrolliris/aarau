from collections.abc import Mapping

import pytest

from webob.multidict import MultiDict, NestedMultiDict, NoVars
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.models import Site


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


# -- GET site_new (publication)

def test_publication_site_new_get_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'publication',
    })
    dummy_request.matchdict = {
        'namespace': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_new(dummy_request)


def test_publication_site_new_get(users, dummy_request):
    from aarau.views.console.site.form import build_new_publication_site_form
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'publication',
    })
    # this an assignment is needed to avoid error form building (must be empty)
    dummy_request.POST = NoVars()
    project = user.projects[0]
    dummy_request.matchdict = {
        'namespace': project.namespace,
    }

    res = site_new(dummy_request)
    form = build_new_publication_site_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


# -- POST site_new (publication)

def test_publication_site_new_post_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    query_param = {'type': 'publication'}
    submit_body = {
        'submit': 'Create',
        # rest is omitted
    }
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'namespace': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_new(dummy_request)


def test_publication_site_new_post_with_validation_error(users, dummy_request):
    from aarau.views.console.site.form import build_new_publication_site_form
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    project = user.projects[0]
    query_param = {'type': 'publication'}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        # invalid values
        'slug': '',
        'publication-name': '',
        'publication-classification': '',
        'publication-license': '',
        'publication-copyright': '2017 Oswald & Weenie',
        'publication-description': '',
        'submit': 'Create',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = NestedMultiDict({**query_param, **submit_body})
    dummy_request.matchdict = {
        'namespace': project.namespace
    }

    res = site_new(dummy_request)
    form = build_new_publication_site_form(dummy_request)

    assert dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form', 'project', 'site') == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert isinstance(res['site'], Site)


def test_publication_site_new_post(mocker, users, dummy_request):
    # pylint: disable=too-many-locals
    from aarau.models import Classification, License
    from aarau.views.console.site.action import site_new

    user = users['oswald']
    project = user.projects[0]

    # pylint: disable=unsubscriptable-object
    license_id = list(License.as_choices)[0][0]
    classification_id = list(Classification.as_choices)[0][0]

    query_param = {'type': 'publication'}
    submit_body = {
        'csrf_token': dummy_request.session.get_csrf_token(),
        'slug': 'new-piano-publication',
        'publication-name': 'New Piano Publication',
        'publication-license': license_id,
        'publication-classification': classification_id,
        'publication-copyright': '2017 Oswald & Weenie',
        'publication-description': '...',
        'submit': 'Create',
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

    assert 1 == len(project.publications)

    res = site_new(dummy_request)

    assert dummy_request.session.peek_flash('success')
    assert isinstance(res, HTTPFound)

    project.refresh()
    publications = project.publications
    assert 2 == len(publications)
    assert 1 == len(list(filter(lambda s: s.publication.name ==
                                'New Piano Publication', publications)))

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.replicate.call_count


# -- GET site_overview (publication)


# -- GET site_settings (publication)

def test_publication_site_settings_get_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'publication',
    })
    dummy_request.matchdict = {
        'namespace': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_settings(dummy_request)


def test_publication_site_settings_get_missing_site(
        mocker, users, dummy_request):
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    project = user.projects[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'publication',
    })
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': ''  # invalid
    }

    class DummyService(object):
        # pylint: disable=no-self-use
        def assign(self, *_args, **_kwargs):
            pass

        def replicate(self, *_args, **_kwargs):
            pass

    dummy_service = DummyService()
    mocker.spy(dummy_service, 'assign')
    mocker.spy(dummy_service, 'replicate')

    dummy_request.find_service = (lambda *args, **kwargs: dummy_service)

    with pytest.raises(HTTPNotFound):
        site_settings(dummy_request)

    # pylint: disable=no-member
    assert 0 == dummy_service.assign.call_count
    assert 0 == dummy_service.replicate.call_count


def test_publication_site_settings_get(mocker, users, dummy_request):
    from aarau.views.console.site.form import build_edit_publication_site_form
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    project = user.projects[0]
    site = project.publications[0]
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.params = dummy_request.GET = NestedMultiDict({
        'type': 'publication',
    })
    # this an assignment is needed to avoid error form building (must be empty)
    dummy_request.POST = NoVars()
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': site.slug,
    }

    class DummyService(object):
        # pylint: disable=no-self-use
        def assign(self, *_args, **_kwargs):
            pass

        def replicate(self, *_args, **_kwargs):
            pass

    dummy_service = DummyService()
    mocker.spy(dummy_service, 'assign')
    mocker.spy(dummy_service, 'replicate')

    dummy_request.find_service = (lambda *args, **kwargs: dummy_service)

    res = site_settings(dummy_request)
    form = build_edit_publication_site_form(dummy_request, site)

    assert isinstance(res, Mapping)
    assert ('form', 'instance', 'project', 'site') == \
        tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert site.publication == res['instance']
    assert site == res['site']

    # pylint: disable=no-member
    assert 0 == dummy_service.assign.call_count
    assert 0 == dummy_service.replicate.call_count


# -- POST site_settings (publication)

def test_publication_site_settings_post_missing_project(users, dummy_request):
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    query_param = {'type': 'publication'}
    submit_body = {
        'submit': 'Update',
        # rest is omitted
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = {**query_param, **submit_body}
    dummy_request.matchdict = {
        'namespace': '',  # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_settings(dummy_request)


def test_publication_site_settings_post_missing_site(users, dummy_request):
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    project = user.projects[0]
    query_param = {'type': 'publication'}
    submit_body = {
        'submit': 'Update',
        # rest is omitted
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = {**query_param, **submit_body}
    dummy_request.matchdict = {
        'namespace': project.namespace,
        # invalid
    }

    with pytest.raises(HTTPNotFound):
        site_settings(dummy_request)


def test_publication_site_settings_post_with_validation_error(
        users, dummy_request):
    from aarau.views.console.site.form import build_edit_publication_site_form
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    project = user.projects[0]
    site = project.publications[0]
    query_param = {'type': 'publication'}
    submit_body = {
        'submit': 'Update',
        'csrf_token': dummy_request.session.get_csrf_token(),
        # invalid values
        'slug': '',
        'publication-name': '',
        'publication-license': '',
        'publication-classification': '',
        'publication-copyright': '',
        'publication-description': '',
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = {**query_param, **submit_body}
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': site.slug,
    }

    res = site_settings(dummy_request)
    form = build_edit_publication_site_form(dummy_request, site)

    assert dummy_request.session.peek_flash('failure')
    assert isinstance(res, Mapping)
    assert ('form', 'instance', 'project', 'site') == \
        tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
    assert project == res['project']
    assert site.publication == res['instance']
    assert site == res['site']


def test_publication_site_settings_post(mocker, users, dummy_request):
    from aarau.views.console.site.action import site_settings

    # edit
    user = users['oswald']
    project = user.projects[0]
    site = project.publications[0]
    publication = site.publication
    query_param = {'type': 'publication'}
    submit_body = {
        'submit': 'Update',
        'csrf_token': dummy_request.session.get_csrf_token(),
        # invalid values
        'slug': site.slug,
        'publication-name': 'New Piano Club Changelog',
        'publication-license': publication.license.id,
        'publication-classification': publication.classification.id,
        'publication-copyright': publication.copyright,
        'publication-description': publication.description,
    }
    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.POST = MultiDict(submit_body)
    dummy_request.params = {**query_param, **submit_body}
    dummy_request.matchdict = {
        'namespace': project.namespace,
        'slug': site.slug,
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

    res = site_settings(dummy_request)

    assert dummy_request.session.peek_flash('success')
    assert isinstance(res, dict)

    publication_name = site.publication.name

    site.refresh()
    site.publication.refresh()

    assert publication.id == site.publication.id
    assert publication_name != site.publication.name

    # pylint: disable=no-member
    assert 1 == dummy_service.assign.call_count
    assert 1 == dummy_service.replicate.call_count
