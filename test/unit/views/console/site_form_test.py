import pytest

from webob.multidict import MultiDict
from aarau.views.console.site.form import (
    build_new_application_site_form,
    NewSiteForm,
)


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    pass


def test_build_new_application_site_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_new_application_site_form(dummy_request)
    assert isinstance(form, NewSiteForm)


@pytest.mark.parametrize('domain', [
    'invalid',
    '-three.org',
    'a.b.c',
    'comma,com',
    'not.-valid.com',
])
def test_validate_domain_format_with_invalid_domain(domain, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'domain': domain,
        'application-name': 'Test Site',
    })
    form = build_new_application_site_form(dummy_request)
    assert not form.validate()
    assert ['Invalid input.'] == form.domain.errors


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
        'application-name': 'Test Site',
    })
    form = build_new_application_site_form(dummy_request)
    assert form.validate()
    assert not form.domain.errors
