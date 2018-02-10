from datetime import datetime

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms import validators as v
from wtforms import ValidationError

from aarau.views.form import (
    USERNAME_PATTERN,
    PASSWORD_PATTERN,
    _,
    SecureForm,
    build_form,
)


def validate_username_uniqueness(_form, field):
    """Unique username check in db."""
    from ...models.user import User
    user = User.select().where(
        User.username == field.data).first()
    if user:
        raise ValidationError('This username is already taken')


def validate_email_uniqueness(_form, field):
    """Unique email address check in db."""
    from ...models.user_email import UserEmail
    user_email = UserEmail.select().where(
        (UserEmail.email == field.data) &
        ((UserEmail.activation_token_expires_at >= datetime.utcnow()) |
         (UserEmail.activation_state == 'active'))).first()
    if user_email:
        raise ValidationError('The email address is already registered')


class SignupForm(SecureForm):
    email = StringField(_('signup.label.email'), [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
        validate_email_uniqueness,
    ])
    name = StringField(_('signup.label.name'), [
        v.Optional(),
        v.Length(min=4, max=32),
    ])
    username = StringField(_('signup.label.username'), [
        v.Optional(),
        v.Regexp(USERNAME_PATTERN, message=(
            'You must use only lowercase alphanumeric characters, and '
            'start with a-z')),
        v.Length(min=4, max=12),
        validate_username_uniqueness,
    ])
    password = PasswordField(_('signup.label.password'), [
        v.Required(),
        v.Regexp(PASSWORD_PATTERN),
        v.Length(min=8, max=32)
    ])
    submit = SubmitField(_('signup.submit.create'))


def build_signup_form(request):
    return build_form(SignupForm, request)
