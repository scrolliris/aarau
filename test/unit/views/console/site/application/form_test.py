import pytest

from webob.multidict import MultiDict

from aarau.views.console.site.form import (
    build_new_application_site_form,
    NewApplicationSiteForm,
)


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    pass


def test_build_new_application_site_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_new_application_site_form(dummy_request)
    assert isinstance(form, NewApplicationSiteForm)


@pytest.mark.parametrize('domain', [
    'invalid',
    '-three.org',
    'a.b.c',  # too short
    'comma,com',
    'not.-valid.com',  # invalid format
    # too long
    'super.loooooooooooooooooooooooooooooooooooooooooooooooooooong.com',
])
def test_validate_domain_format_with_invalid_domain(domain, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': domain,
        'application-name': 'Test Site',
    })
    form = build_new_application_site_form(dummy_request)
    assert not form.validate()
    assert form.domain.errors


@pytest.mark.parametrize('domain', [
    'about.scrolliris.com',
    'scrolliris.com',
    'lupine-software.com',
    'amzn.to',
    'goo.gl',
])
def test_validate_domain_format_with_valid_domain(domain, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': domain,
        'slug': 'test-site',
        'application-name': 'Test Site',
    })
    form = build_new_application_site_form(dummy_request)
    assert form.validate()
    assert not form.domain.errors


@pytest.mark.parametrize('slug', [
    'help',  # too short
    '-abcde',  # invalid char
    'under_score',
    'abc--de',  # sequencial hyphens
    'abc--',
    '--abc',
    '001-slug',  # non-alphabet at start
    'scrolliris',  # reserved
    'loooooooooooooooooooooooooooooong',  # too long
])
def test_validate_slug_format_with_invalid_slug(slug, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'slug': slug,
        'domain': 'example.org',
        'application-name': 'New site',
    })
    form = build_new_application_site_form(dummy_request)
    assert not form.validate()
    assert form.slug.errors


@pytest.mark.parametrize('slug', [
    'abcdef',
    'a-b-c-d-e',
    'lorem-ipsum',
    'slug-01',
    'one-slug-two',
    'looooooooooooooooooooooooooooong',
])
def test_validate_slug_format_with_valid_slug(slug, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'slug': slug,
        'domain': 'example.org',
        'application-name': 'New site',
    })
    form = build_new_application_site_form(dummy_request)
    assert form.validate()
    assert not form.slug.errors
