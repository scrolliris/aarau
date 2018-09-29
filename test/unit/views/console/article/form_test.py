import pytest
from webob.multidict import MultiDict
from wtforms import ValidationError

from aarau.models.article import Article
from aarau.views.console.article.form import (
    build_article_settings_form,
    build_article_editor_form,
    path_duplication_check,
    path_availability_check,
    ArticleEditorForm,
    ArticleSettingsForm,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views import form
    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_build_article_settings_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    article = Article()
    form = build_article_settings_form(dummy_request, article)
    assert isinstance(form, ArticleSettingsForm)


def test_build_article_editor_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    article = Article()
    form = build_article_editor_form(dummy_request, article)
    assert isinstance(form, ArticleEditorForm)


def test_path_duplication_check(mocker, users, dummy_request):
    user = users['oswald']
    article = Article()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_article_settings_form(dummy_request, article)

    with pytest.raises(ValidationError):
        user = users['oswald']
        existing_article = user.articles[0]
        field = mocker.Mock('field', data=existing_article.path)
        path_duplication_check(form, field)


def test_path_availability_check(mocker, dummy_request):
    article = Article(path='scrolliris')

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_article_settings_form(dummy_request, article)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=article.path)
        path_availability_check(form, field)


@pytest.mark.parametrize('path', [
    'abc',  # too short
    'aBcdef',  # invalid char
    '-abcde',
    'under_score',
    'abc--de',  # sequencial hyphens
    'abc--',
    '--abc',
    'scrolliris',  # reserved
    # too long
    'super-looooooooooooooooooooooooooooooooooooooooooooooooooong-path',
])
@pytest.mark.parametrize('scope', ['public', 'private'])
@pytest.mark.parametrize('progress_state', (
    {'value': '0', 'label': 'draft'},
    {'value': '1', 'label': 'wip'},
    {'value': '2', 'label': 'ready'},
    {'value': '6', 'label': 'archived'},
))
def test_path_validations_with_invalid_path_inputs(
        path, scope, progress_state, dummy_request):
    article = Article(path=path)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
        'scope': scope,
        'progress_state': progress_state['value'],
    })
    form = build_article_settings_form(dummy_request, article)
    assert not form.validate()
    assert form.path.errors


@pytest.mark.parametrize('path', ['abcdef', 'a-b-c-d-e'])
@pytest.mark.parametrize('scope', ['public', 'private'])
@pytest.mark.parametrize('progress_state', (
    {'value': '3', 'label': 'scheduled'},
    {'value': '4', 'label': 'published'},
    {'value': '5', 'label': 'rejected'},
    {'value': '9', 'label': 'unknown'},
))  # not available state for draft
def test_path_validations_with_invalid_progress_state_inputs(
        path, scope, progress_state, dummy_request):
    article = Article(path=path)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
        'scope': scope,
        'progress_state': progress_state['value'],
    })
    form = build_article_settings_form(dummy_request, article)
    assert not form.validate()
    assert form.progress_state.errors


@pytest.mark.parametrize('path', [
    'abcdef',
    'a-b-c-d-e',
    'lorem-ipsum',
    'chapter-01',
    '001-article-title',
    'super-loooooooooooooooooooooooooooooooooooooooooooooooooong-path',
])
@pytest.mark.parametrize('scope', ['public', 'private'])
@pytest.mark.parametrize('progress_state', (
    {'value': '0', 'label': 'draft'},
    {'value': '1', 'label': 'wip'},
    {'value': '2', 'label': 'ready'},
    {'value': '6', 'label': 'archived'},
))  # draft
def test_path_validations_with_valid_path_inputs(
        path, scope, progress_state, dummy_request):
    article = Article(path=path)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
        'scope': scope,
        'progress_state': progress_state['value'],
    })
    form = build_article_settings_form(dummy_request, article)
    assert form.validate()
    assert not form.path.errors
