from wtforms import (
    FormField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v
from wtforms.form import Form

from aarau.views.form import SecureForm, build_form

DOMAIN_PATTERN = r'\A([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}' \
    r'[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}\Z'


class SiteFormBaseMixin(object):
    domain = StringField('Domain', [
        v.Required(),
        v.Regexp(DOMAIN_PATTERN),
        v.Length(min=3, max=64),
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


class EditSiteForm(SiteFormBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Update')


def build_new_application_site_form(req):
    return build_form(NewSiteForm, req)


def build_edit_application_site_form(req):
    return build_form(EditSiteForm, req)
