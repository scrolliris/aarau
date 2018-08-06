import pytest

from webob.multidict import MultiDict


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    pass


def test_build_new_application_site_form(dummy_request):
    from aarau.views.console.site.form import (
        build_new_application_site_form,
        NewApplicationSiteForm,
    )

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
    from aarau.views.console.site.form import build_new_application_site_form

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
    from aarau.views.console.site.form import build_new_application_site_form

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
    'foo-bar-baz-qux-quux' * 3,  # too long
    'under_score',  # invalid format
    '0-foo-bar',  # invalid format
])
def test_validate_slug_format_with_invalid_slug(slug, dummy_request):
    from aarau.views.console.site.form import build_new_application_site_form

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': 'example.com',
        'slug': slug,
        'application-name': 'Test Site',
    })
    form = build_new_application_site_form(dummy_request)
    assert not form.validate()
    assert form.slug.errors
