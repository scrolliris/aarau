from wtforms import (
    FormField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v, ValidationError
from wtforms.form import Form

from aarau.views.form import SecureForm, build_form

DOMAIN_PATTERN = r'\A([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}' \
    r'[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}\Z'

SLUG_PATTERN = r'\A[A-Za-z0-9-]{0,32}\Z'


class ApplicationBaseMixin(object):
    domain = StringField('Domain', [
        v.Required(),
        v.Regexp(DOMAIN_PATTERN),
        v.Length(min=3, max=32),
    ])

    slug = StringField('Slug', [
        v.Optional(),
        v.Regexp(SLUG_PATTERN),
        v.Length(min=6, max=32),
    ])


class PublicationBaseMixin(object):
    slug = StringField('Slug', [
        v.Required(),
        v.Regexp(SLUG_PATTERN),
        v.Length(min=6, max=32),
    ])

    def validate_slug(self, field):   # pylint: disable=no-self-use
        from aarau.models.site import Site

        query = Site.select().where(
            Site.domain >> None,
            Site.slug == field.data)
        if hasattr(self, 'current_site'):
            # allow itself
            query = query.where(
                Site.id != self.current_site.id)
        if query.first():
            raise ValidationError('Slug is already taken.')


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


# nested form
class PublicationForm(Form):
    classification = SelectField('Classification', [
        v.Required(),
    ], choices=(...))
    name = StringField('Name', [
        v.Required(),
        v.Length(min=3, max=64),
    ])
    copyright = StringField('Copyright', [
        v.Required(),
        v.Length(min=3, max=255),
    ])
    description = TextAreaField('Description', [
        v.Optional(),
        v.Length(max=255),
    ])

    @staticmethod
    def __classification_choices():
        """Returns classification choices generator as list.

        Because it seems that wtforms SelectField's choices needs list.
        If returns just iterable or generator, it does not work at re-rendering
        after submit.
        """
        from aarau.models import Classification

        return list(Classification.as_choices)

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        # pylint: disable=no-member
        self.classification.kwargs['choices'] = self.__classification_choices()

        super().__init__(formdata, obj, prefix, **kwargs)


# application

class NewApplicationSiteForm(ApplicationBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Create')


class EditApplicationSiteForm(ApplicationBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Update')


def build_new_application_site_form(req):
    return build_form(NewApplicationSiteForm, req)


def build_edit_application_site_form(req, site):
    return build_form(EditApplicationSiteForm, req, site)


# publication

class NewPublicationSiteForm(PublicationBaseMixin, SecureForm):
    publication = FormField(PublicationForm)
    submit = SubmitField('Create')


class EditPublicationSiteForm(PublicationBaseMixin, SecureForm):
    publication = FormField(PublicationForm)
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._site = None

    @property
    def current_site(self):
        return self._site

    @current_site.setter
    def current_site(self, site):
        self._site = site


def build_new_publication_site_form(req):
    return build_form(NewPublicationSiteForm, req)


def build_edit_publication_site_form(req, site):
    form = build_form(EditPublicationSiteForm, req, site)
    form.current_site = site
    return form
