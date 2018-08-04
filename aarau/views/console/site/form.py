from wtforms import (
    FormField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v, ValidationError
from wtforms.form import Form

from aarau.views.form import (
    SecureForm,
    build_form,
    availability_checker,
)

DOMAIN_PATTERN = r'\A([A-z0-9]\.|[A-z0-9][A-z0-9-]{0,61}' \
    r'[A-z0-9]\.){1,3}[A-z]{2,6}\Z'
SLUG_PATTERN = r'\A[A-z]([A-Za-z0-9-]{5,31})\Z'


def slug_availability_check(form, field):
    checker = availability_checker('site.slug')
    return checker(form, field)


class SiteInstanceMixin(object):
    slug = StringField('Slug', [
        v.Required(),
        v.Regexp(SLUG_PATTERN),
        v.Length(min=6, max=32),
        slug_availability_check,
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._site = None

    @property
    def current_site(self):
        return self._site

    @current_site.setter
    def current_site(self, site):
        self._site = site

    def validate_slug(self, field):   # pylint: disable=no-self-use
        from aarau.models.site import Site

        query = Site.select().where(
            Site.slug == field.data)
        if hasattr(self, 'current_site') and self.current_site:
            # allow itself
            query = query.where(
                Site.id != self.current_site.id)
        if query.first():
            raise ValidationError('Slug is already taken.')


class SiteForm(object):
    class ApplicationBaseMixin(SiteInstanceMixin):
        domain = StringField('Domain', [
            v.Required(),
            v.Regexp(DOMAIN_PATTERN),
            v.Length(min=3, max=32),
        ])

    class PublicationBaseMixin(SiteInstanceMixin):
        pass


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
    license = SelectField('License', [
        v.Required(),
    ], choices=(...))
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

    @staticmethod
    def __license_choices():
        """Returns license choices generator as list.

        Because it seems that wtforms SelectField's choices needs list.
        If returns just iterable or generator, it does not work at re-rendering
        after submit.
        """
        from aarau.models import License

        return list(License.as_choices)

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        # pylint: disable=no-member
        self.classification.kwargs['choices'] = self.__classification_choices()
        self.license.kwargs['choices'] = self.__license_choices()

        super().__init__(formdata, obj, prefix, **kwargs)


# application

class NewApplicationSiteForm(SiteForm.ApplicationBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Create')

    @property
    def instance(self):
        return getattr(self, 'application')  # alias


class EditApplicationSiteForm(SiteForm.ApplicationBaseMixin, SecureForm):
    application = FormField(ApplicationForm)
    submit = SubmitField('Update')

    @property
    def instance(self):
        return getattr(self, 'application')  # alias


def build_new_application_site_form(req):
    return build_form(NewApplicationSiteForm, req)


def build_edit_application_site_form(req, site):
    form = build_form(EditApplicationSiteForm, req, site)
    form.current_site = site
    return form


# publication

class NewPublicationSiteForm(SiteForm.PublicationBaseMixin, SecureForm):
    publication = FormField(PublicationForm)
    submit = SubmitField('Create')

    @property
    def instance(self):
        return getattr(self, 'publication')  # alias


class EditPublicationSiteForm(SiteForm.PublicationBaseMixin, SecureForm):
    publication = FormField(PublicationForm)
    submit = SubmitField('Update')

    @property
    def instance(self):
        return getattr(self, 'publication')  # alias


def build_new_publication_site_form(req):
    return build_form(NewPublicationSiteForm, req)


def build_edit_publication_site_form(req, site):
    form = build_form(EditPublicationSiteForm, req, site)
    form.current_site = site
    return form


def build_site_form(req, site=None):
    from aarau.models import Site
    try:
        if not isinstance(site, Site):
            raise AttributeError
        if site.is_dirty():
            if site.type == 'application':
                return build_new_application_site_form(req)
            elif site.type == 'publication':
                return build_new_publication_site_form(req)
        if site.type == 'application':
            return build_edit_application_site_form(req, site)
        elif site.type == 'publication':
            return build_edit_publication_site_form(req, site)
        return None
    except AttributeError:
        return None
