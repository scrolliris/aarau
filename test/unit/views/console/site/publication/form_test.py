import pytest

from webob.multidict import MultiDict

from aarau.models.classification import Classification
from aarau.models.license import License
from aarau.views.console.site.form import (
    build_new_publication_site_form,
    NewPublicationSiteForm,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views import form
    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_build_new_publication_site_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_new_publication_site_form(dummy_request)
    assert isinstance(form, NewPublicationSiteForm)


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
    classification_id = next(Classification.as_choices)[0]
    license_id = next(License.as_choices)[0]

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'slug': slug,
        'domain': None,
        'publication-name': 'New site',
        'publication-copyright': 'copyright',
        'publication-classification': classification_id,
        'publication-license': license_id,
    })
    form = build_new_publication_site_form(dummy_request)
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
    classification_id = next(Classification.as_choices)[0]
    license_id = next(License.as_choices)[0]

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'slug': slug,
        'domain': None,
        'publication-name': 'New site',
        'publication-copyright': 'copyright',
        'publication-classification': classification_id,
        'publication-license': license_id,
    })
    form = build_new_publication_site_form(dummy_request)
    assert form.validate()
    assert not form.slug.errors
