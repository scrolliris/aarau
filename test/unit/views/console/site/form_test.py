import pytest
from webob.multidict import MultiDict
from wtforms import ValidationError

from aarau.models.site import Site
from aarau.views.console.site.form import (
    build_site_form,
    slug_availability_check,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views import form
    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_slug_availability_check(mocker, dummy_request):
    site = Site(instance_type='Application', slug='scrolliris')

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_site_form(dummy_request, site)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=site.slug)
        slug_availability_check(form, field)
