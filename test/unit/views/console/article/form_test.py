import pytest
from webob.multidict import MultiDict
from wtforms import ValidationError

from aarau.models.article import Article
from aarau.views.console.article.form import (
    build_article_config_form,
    build_article_editor_form,
    path_duplication_check,
    path_availability_check,
    ArticleConfigForm,
    ArticleEditorForm,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views import form
    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_build_article_config_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    article = Article()
    form = build_article_config_form(dummy_request, article)
    assert isinstance(form, ArticleConfigForm)


def test_build_article_editor_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    article = Article()
    form = build_article_editor_form(dummy_request, article)
    assert isinstance(form, ArticleEditorForm)


def test_path_duplication_check(mocker, users, dummy_request):
    user = users['oswald']
    article = Article()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_article_config_form(dummy_request, article)

    with pytest.raises(ValidationError):
        user = users['oswald']
        existing_article = user.articles[0]
        field = mocker.Mock('field', data=existing_article.path)
        path_duplication_check(form, field)


def test_path_availability_check(mocker, dummy_request):
    article = Article(path='scrolliris')

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_article_config_form(dummy_request, article)

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
def test_path_validations_with_invalid_inputs(path, dummy_request):
    article = Article(path=path)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
    })
    form = build_article_config_form(dummy_request, article)
    assert not form.validate()
    assert form.path.errors


@pytest.mark.parametrize('path', [
    'abcdef',
    'a-b-c-d-e',
    'lorem-ipsum',
    'chapter-01',
    '001-article-title',
    'super-loooooooooooooooooooooooooooooooooooooooooooooooooong-path',
])
def test_path_validations_with_valid_inputs(path, dummy_request):
    article = Article(path=path)

    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
    })
    form = build_article_config_form(dummy_request, article)
    assert form.validate()
    assert not form.path.errors
