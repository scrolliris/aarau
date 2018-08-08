import itertools
import yaml

from pyramid.i18n import TranslationStringFactory
from pyramid.path import AssetResolver
from wtforms import ValidationError
from wtforms.form import Form
from wtforms.csrf.core import CSRF as _CSRF

RESERVED_WORDS_FILE = 'aarau:../config/reserved_words.yml'


def availability_checker(key):
    """Check user input with reserved words loaded from yml file."""
    keys = key.split('.')
    if len(keys) != 2:
        raise RuntimeError

    def _check_availability(_form, field):
        a = AssetResolver('aarau')
        resolver = a.resolve(RESERVED_WORDS_FILE)
        try:
            with open(resolver.abspath(), 'r') as f:
                data = yaml.safe_load(f).get('reserved_words', {})
                reserved_words = set(itertools.chain(
                    data.get('common', []),
                    data.get(keys[0], {}).get(keys[1], []),
                ))
                # TODO: translate
                if field.data in reserved_words:
                    raise ValidationError(
                        '{} is unavailable.'.format(keys[1].title()))
        except FileNotFoundError:
            pass

    return _check_availability


_ = TranslationStringFactory('form')


class CSRF(_CSRF):
    """CSRF utility extends pyramid's builtin csrf."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csrf_context = None

    def setup_form(self, form):
        self.csrf_context = form.meta.csrf_context
        return super(CSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_token_field):
        return self.csrf_context.get_csrf_token()

    def validate_csrf_token(self, form, field):
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')


PASSWORD_PATTERN = r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])'
USERNAME_PATTERN = r'\A[a-z][a-z0-9\_\-]+\Z'
USERNAME_PATTERN_INVALID = r'\A((?!--).)*\Z'


class SecureForm(Form):  # pylint: disable=too-few-public-methods
    """Form base class enables csrf protection."""

    class Meta:
        csrf = True
        csrf_class = CSRF


class FailureForm(SecureForm):
    """A form returns always failure at its validation."""

    def validate(self):
        return False


def build_form(klass, req, obj=None):
    """Builder method builds a form."""
    form = klass(req.POST, obj, meta={
        'csrf_context': req.session,
        'locales': ['en_US', 'en'],
    })
    return form
