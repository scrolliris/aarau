import pytest

from aarau.models import Article


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_generate_code_returns_fixed_length_string():
    code = Article.generate_code()
    assert 40 == len(code)


def test_generate_code_returns_valid_sha1_string():
    import re

    code = Article.generate_code()
    assert re.match(r'^[0-9a-f]{40}$', code)


def test_generate_code_returns_always_new_code():
    codes = [c for c in filter(
        lambda x: Article.generate_code(), range(5))]
    assert 5 == len(set(codes))


def test_grab_unique_code_repeats_until_to_grab_unique_code(
        articles, mocker):
    article = articles['piano-lesson']

    codes = ['brand-new-sha1-code', article.code]

    def dummy_generate_code():
        return codes.pop()

    # this patch restores original method after test case
    mocker.patch.object(Article, 'generate_code')
    Article.generate_code = dummy_generate_code

    # to spy called count
    mocker.spy(Article, 'generate_code')
    mocker.spy(Article, 'get')

    code = Article.grab_unique_code()

    # pylint: disable=no-member
    assert 2 == Article.generate_code.call_count
    assert 2 == Article.get.call_count

    assert 'brand-new-sha1-code' == code
    assert article.code != code


def test_published_at_assignment_by_save(users):
    from datetime import datetime
    from aarau.models import Project, Site

    user = users['oswald']
    project = user.projects.where(
        Project.namespace == 'piano-music-club').get()
    site = project.sites.where(Site.instance_type == 'Publication').get()

    attrs = {
        'publication': site.publication,
        'path': 'spring-concret',
        'title': 'Spring Concert',
        'copyright': '2017 Oswald & Weenie',
        'progress_state': 'draft'
    }
    article = Article(**attrs)
    article.code = Article.grab_unique_code()
    article.save()
    assert None is article.published_at

    article.progress_state = 'published'
    article.save()
    assert isinstance(article.published_at, datetime)


def test_progress_state_as_choises():
    expected_choices = [
        ('draft', 'draft'),
        ('wip', 'wip'),
        ('ready', 'ready'),
        ('scheduled', 'scheduled'),
        ('published', 'published'),
        ('rejected', 'rejected'),
        ('archived', 'archived'),
    ]
    assert expected_choices == Article.progress_state_as_choices


def test_published_on(publications):
    publication = publications['How to score music playing piano']
    articles = Article.published_on(publication)
    article = next((a for a in articles), None)

    assert articles
    assert isinstance(article, Article)
