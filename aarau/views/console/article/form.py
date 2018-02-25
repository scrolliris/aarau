import itertools
import yaml

from pyramid.path import AssetResolver
from wtforms import (
    StringField,
    SubmitField,
)
from wtforms import validators as v, ValidationError

from aarau.views.form import SecureForm, build_form


PATH_PATTERN = r'\A[a-z0-9]{1}[a-z0-9-]+\Z'
RESERVED_WORDS_FILE = 'aarau:../config/reserved_words.yml'


def path_duplication_check(form, field):
    from aarau.models.article import Article

    query = Article.select().where(
        Article.path == field.data)
    if hasattr(form, 'current_article') and form.current_article:
        # allow itself
        query = query.where(
            Article.id != form.current_article.id)
    if query.first():
        raise ValidationError('That path is already in use.')


def path_reserved_words_check(_form, field):
    """Check user input with reserved words loaded from yml file."""
    a = AssetResolver('aarau')
    resolver = a.resolve(RESERVED_WORDS_FILE)
    try:
        with open(resolver.abspath(), 'r') as f:
            data = yaml.safe_load(f).get('reserved_words', {})
            reserved_words = set(itertools.chain(
                data.get('common', []),
                data.get('article', {}).get('path', []),
            ))
            if field.data in reserved_words:
                raise ValidationError('That path is unavailable.')
    except FileNotFoundError:
        pass


class ArticleBaseMixin(object):
    title = StringField('Title', [
        v.Required(),
        v.Length(min=3, max=128),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._article = None

    @property
    def current_article(self):
        return self._article

    @current_article.setter
    def current_article(self, article):
        self._article = article


class NewArticleForm(ArticleBaseMixin, SecureForm):
    path = StringField('Path', [
        v.Required(),
        v.Regexp(PATH_PATTERN),
        v.Length(min=6, max=64),
        path_duplication_check,
        path_reserved_words_check,
    ])

    submit = SubmitField('Create')


class EditArticleForm(ArticleBaseMixin, SecureForm):
    submit = SubmitField('Update')


def build_new_article_form(req):
    return build_form(NewArticleForm, req)


def build_edit_article_form(req, article):
    form = build_form(EditArticleForm, req, article)
    form.current_article = article
    return form


def build_article_form(req, article=None):
    from aarau.models import Article
    try:
        if not isinstance(article, Article):
            raise AttributeError

        if article.is_dirty():
            return build_new_article_form(req)

        return build_edit_article_form(req, article)
    except AttributeError:
        return None
