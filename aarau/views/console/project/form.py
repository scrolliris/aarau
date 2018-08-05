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
    availability_checker,
)

NAMESPACE_PATTERN = r'\A[a-z][a-z0-9\-]+[a-z0-9]\Z'


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


def namespace_availability_check(form, field):
    checker = availability_checker('project.namespace')
    return checker(form, field)


class ProjectFormBaseMixin(object):
    name = StringField('Name', [
        v.Required(),
        v.Length(min=6, max=32),
    ])
    namespace = StringField('Namespace', [
        v.Required(),
        v.Regexp(NAMESPACE_PATTERN),
        v.Length(min=4, max=16),
        namespace_duplication_check,
        namespace_availability_check,
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
    ], choices=())  # delay

    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        self.__class__.plan.choices = Plan.as_choices

        super().__init__(*args, **kwargs)


def build_new_project_form(req):
    return build_form(NewProjectForm, req)


def build_edit_project_form(req, project):
    form = build_form(EditProjectForm, req, project)
    form.current_project = project
    return form


def build_project_form(req, project=None):
    from aarau.models import Project

    try:
        if not isinstance(project, Project):
            raise AttributeError

        if project.is_dirty():
            return build_new_project_form(req)

        return build_edit_project_form(req, project)
    except AttributeError:
        return None
