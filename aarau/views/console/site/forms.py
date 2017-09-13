from wtforms import (
    FormField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v, ValidationError
from wtforms.form import Form

from aarau.views.forms import SecureForm, build_form


class SiteFormBaseMixin(object):
    domain = StringField('Domain', [
        v.Required(),
        v.Length(min=3, max=32),
    ])


# nested form
class ApplicationForm(Form):
    name = StringField('Name', [
        v.Required(),
        v.Length(min=3, max=64),
    ])
    description = TextAreaField('Description', [
        v.Optional(),
        v.Length(max=255),
    ])


class NewSiteForm(SiteFormBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Create')


def new_application_site_form(req, project):
    class ANewSiteForm(NewSiteForm):
        def validate_domain(self, field):
            from aarau.models.site import Site
            site = Site.select().where(
                Site.hosting_type == 'Application',
                Site.project_id == project.id,  # pylint: disable=no-member
                Site.domain == field.data).first()
            if site:
                raise ValidationError('Domain already exists.')

    return build_form(ANewSiteForm, req)


class EditSiteForm(SiteFormBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Update')


def edit_application_site_form(req, project, site):
    class AnEditSiteForm(EditSiteForm):
        pass

    return build_form(AnEditSiteForm, req, site)
