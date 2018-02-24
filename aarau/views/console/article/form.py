from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v, ValidationError

from aarau.views.form import SecureForm, build_form


PATH_PATTERN = r'\A[a-z0-9-]+\Z'


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

    def validate_path(self, field):   # pylint: disable=no-self-use
        from aarau.models.article import Article

        query = Article.select().where(
            Article.path == field.data)
        if hasattr(self, 'current_article') and self.current_article:
            # allow itself
            query = query.where(
                Article.id != self.current_article.id)
        if query.first():
            raise ValidationError('This path is already in use.')


class NewArticleForm(ArticleBaseMixin, SecureForm):
    path = StringField('Path', [
        v.Required(),
        v.Regexp(PATH_PATTERN),
        v.Length(min=6, max=64),
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
