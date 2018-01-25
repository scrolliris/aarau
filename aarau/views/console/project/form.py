import itertools
import yaml

from pyramid.path import AssetResolver
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
    validators as v,
)

from aarau.models import Plan
from aarau.views.form import (
    SecureForm,
    build_form,
)


NAMESPACE_PATTERN = r'\A[a-z][a-z0-9\-]+[a-z0-9]\Z'
RESERVED_WORDS_FILE = 'aarau:../config/reserved_words.yml'


def namespace_duplication_check(form, field):
    from aarau.models.project import Project

    query = Project.select().where(
        Project.namespace == field.data)

    if hasattr(form, 'current_project') and form.current_project:
        # allow itself
        query = query.where(
            Project.id != form.current_project.id)

    if query.first():
        raise ValidationError('Namespace is already taken.')


def namespace_reserved_words_check(_form, field):
    """Check user input with reserved words loaded from yml file."""
    a = AssetResolver('aarau')
    resolver = a.resolve(RESERVED_WORDS_FILE)
    try:
        with open(resolver.abspath(), 'r') as f:
            data = yaml.safe_load(f).get('reserved_words', {})
            reserved_words = set(itertools.chain(
                data.get('common', []),
                data.get('project', {}).get('namespace', []),
            ))
            if field.data in reserved_words:
                raise ValidationError('Namespace is unavailable.')
    except FileNotFoundError:
        pass


class ProjectFormBaseMixin(object):
    name = StringField('Name', [
        v.Required(),
        v.Length(min=6, max=32),
    ])
    namespace = StringField('Namespace', [
        v.Required(),
        v.Regexp(NAMESPACE_PATTERN),
        v.Length(min=6, max=32),
        namespace_duplication_check,
        namespace_reserved_words_check,
    ])
    description = TextAreaField('Description', [
        v.Optional(),
        v.Length(max=1600),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._project = None

    @property
    def current_project(self):
        return self._project

    @current_project.setter
    def current_project(self, project):
        self._project = project


class NewProjectForm(ProjectFormBaseMixin, SecureForm):
    submit = SubmitField('Create')


class EditProjectForm(ProjectFormBaseMixin, SecureForm):
    plan = SelectField('Plan', [
        v.Required(),
    ], choices=Plan.as_choices)

    submit = SubmitField('Update')


def build_new_project_form(req):
    return build_form(NewProjectForm, req)


def build_edit_project_form(req, project):
    form = build_form(EditProjectForm, req, project)
    form.current_project = project
    return form
