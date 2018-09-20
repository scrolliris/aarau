from wtforms import (
    FormField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import Form
from wtforms import validators as v, ValidationError

from aarau.views.form import (
    SecureForm,
    build_form,
    availability_checker,
)

DOMAIN_PATTERN = r'\A([a-z0-9]\.|[a-z0-9][a-z0-9-]{0,61}' \
    r'[a-z0-9]\.){1,3}[a-z]{2,6}\Z'
SLUG_PATTERN = r'\A[A-Za-z][A-Za-z0-9\-]+[A-Za-z0-9]\Z'
SLUG_PATTERN_INVALID = r'\A((?!--).)*\Z'


def slug_availability_check(form, field):
    checker = availability_checker('site.slug')
    return checker(form, field)


class SiteInstanceMixin():
    slug = StringField('Slug', [
        v.Required(),
        v.Regexp(SLUG_PATTERN),
        v.Regexp(SLUG_PATTERN_INVALID),
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

        # pylint: disable=assignment-from-no-return
        query = Site.select().where(
            Site.slug == field.data)

        if hasattr(self, 'current_site') and self.current_site:
            # allow itself
            query = query.where(
                Site.id != self.current_site.id)

        if query.first():
            raise ValidationError('Slug is already taken.')


# nested form (for FormField)
class ApplicationInnerForm(Form):
    name = StringField('Name', [
        v.Required(),
        v.Length(min=3, max=64),
    ])
    description = TextAreaField('Description', [
        v.Optional(),
        v.Length(max=255),
    ])


# nested form (for FormField)
class PublicationInnerForm(Form):
    classification = HiddenField('Classification', [
        v.Required(),
    ])
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
    def __license_choices():
        """Returns license choices generator as list.

        Because it seems that wtforms SelectField's choices needs list.
        If returns just iterable or generator, it does not work at re-rendering
        after submit.
        """
        from aarau.models import License

        return list(License.as_choices)

    def __init__(self, *args, **kwargs):
        # pylint: disable=no-member
        self.license.kwargs['choices'] = self.__license_choices()

        super().__init__(*args, **kwargs)


# application

class NewApplicationSiteForm(SecureForm, SiteInstanceMixin):
    domain = StringField('Domain', [
        v.Required(),
        v.Regexp(DOMAIN_PATTERN),
        v.Length(min=3, max=64),
    ])
    application = FormField(ApplicationInnerForm)
    submit = SubmitField('Create')

    @property
    def instance(self):
        return getattr(self, 'application')  # alias


class EditApplicationSiteForm(SecureForm, SiteInstanceMixin):
    domain = StringField('Domain', [
        v.Required(),
        v.Regexp(DOMAIN_PATTERN),
        v.Length(min=3, max=64),
    ])
    application = FormField(ApplicationInnerForm)
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

class NewPublicationSiteForm(SiteInstanceMixin, SecureForm):
    publication = FormField(PublicationInnerForm)
    submit = SubmitField('Create')

    @property
    def instance(self):
        return getattr(self, 'publication')  # alias


class EditPublicationSiteForm(SiteInstanceMixin, SecureForm):
    publication = FormField(PublicationInnerForm)
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
            if site.type == 'publication':
                return build_new_publication_site_form(req)
        if site.type == 'application':
            return build_edit_application_site_form(req, site)
        if site.type == 'publication':
            return build_edit_publication_site_form(req, site)
        return None
    except AttributeError:
        return None
