from wtforms import (
    BooleanField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v, ValidationError

from aarau.models import Article
from aarau.views.form import (
    SecureForm,
    build_form,
    availability_checker,
)

PATH_PATTERN = r'\A[a-z0-9]{1}[a-z0-9-]+\Z'
PATH_PATTERN_INVALID = r'\A((?!--).)*\Z'


def path_duplication_check(form, field):
    # pylint: disable=assignment-from-no-return
    query = Article.select().where(
        Article.path == field.data)

    if hasattr(form, 'current_article') and form.current_article:
        # allow itself
        query = query.where(
            Article.id != form.current_article.id)
    if query.first():
        raise ValidationError('That path is already in use.')


def path_availability_check(form, field):
    checker = availability_checker('article.path')
    return checker(form, field)


class ArticleBaseMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._article = None

    @property
    def current_article(self):
        return self._article

    @current_article.setter
    def current_article(self, article):
        self._article = article


class ArticleEditorForm(ArticleBaseMixin, SecureForm):
    code = HiddenField([
        v.Required(),
    ])
    content = TextAreaField('Content', [
        v.Optional(),
        v.Length(max=9999),
    ])

    context = HiddenField([
        v.Required(),
        v.AnyOf(('editor',))
    ])
    submit = SubmitField('Save')


def build_article_editor_form(req, article=None):
    form = build_form(ArticleEditorForm, req, article)
    form.current_article = article
    return form


class ArticleSettingsForm(ArticleBaseMixin, SecureForm):
    code = HiddenField([
        v.Required(),
    ])
    title = StringField('Title', [
        v.Required(),
        v.Length(min=3, max=128),
    ])
    scope = BooleanField('Scope', [
        v.Required(),
    ])
    progress_state = SelectField('Progress State', [
        v.Required(),
    ], choices=())  # delay
    path = StringField('Path', [
        v.Required(),
        v.Regexp(PATH_PATTERN),
        v.Regexp(PATH_PATTERN_INVALID),
        v.Length(min=6, max=64),
        path_duplication_check,
        path_availability_check,
    ])
    context = HiddenField([
        v.Required(),
        v.AnyOf(('settings',))
    ])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        # pylint: disable=no-member
        article = args[1]
        self.__class__.progress_state.kwargs['choices'] = \
            article.available_progress_states_as_choices

        super().__init__(*args, **kwargs)


def build_article_settings_form(req, article=None):
    form = build_form(ArticleSettingsForm, req, article)
    form.current_article = article
    return form
