import pytest
from webob.multidict import MultiDict
from wtforms import ValidationError

from aarau.models.article import Article
from aarau.views.console.article.form import (
    build_new_article_form,
    build_edit_article_form,
    path_duplication_check,
    path_reserved_words_check,
    NewArticleForm,
    EditArticleForm,
)


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    pass


def test_build_new_article_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_new_article_form(dummy_request)
    assert isinstance(form, NewArticleForm)


def test_build_edit_article_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    article = Article()
    form = build_edit_article_form(dummy_request, article)
    assert isinstance(form, EditArticleForm)


def test_path_duplication_check(mocker, users, dummy_request):
    user = users['oswald']
    article = user.articles[0]

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_new_article_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=article.path)
        path_duplication_check(form, field)


def test_path_reserved_words_check(mocker, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_new_article_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data='scrolliris')
        path_reserved_words_check(form, field)


@pytest.mark.parametrize('path', [
    'abc',  # too short
    'aBcdef',  # invalid char `B`
    '-abcde',  # invalid char position `-`
    'scrolliris',  # reserved
    # too long
    'super-looooooooooooooooooooooooooooooooooooooooooooooooooong-path',
])
def test_validate_path_with_invalid_inputs(path, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
    })
    form = build_new_article_form(dummy_request)
    assert not form.validate()
    assert form.path.errors


@pytest.mark.parametrize('path', [
    'abcdef',
    'lorem-ipsum',
    'chapter-01',
    '001-article-title',
    'super-loooooooooooooooooooooooooooooooooooooooooooooooooong-path',
])
def test_validate_path_with_valid_inputs(path, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'title': 'Title',
        'path': path,
    })
    form = build_new_article_form(dummy_request)
    assert form.validate()
    assert not form.path.errors
