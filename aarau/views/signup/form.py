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


class SignupFormBase(SecureForm):
    """Base signup form definition."""

    email = StringField(_('signup.label.email'), [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])
    name = StringField(_('signup.label.name'), [
        v.Optional(),
        v.Length(min=2, max=64),
    ])
    username = StringField(_('signup.label.username'), [
        v.Optional(),
        v.Regexp(USERNAME_PATTERN, message=None),
        v.Length(min=4, max=16),
    ])
    password = PasswordField(_('signup.label.password'), [
        v.Required(),
        v.Regexp(PASSWORD_PATTERN),
        v.Length(min=6, max=32)
    ])
    submit = SubmitField(_('signup.submit.create'))


class SignupForm(SignupFormBase):
    # pylint: disable=no-self-use

    def validate_email(self, field):
        """Valites email address existing."""
        from ...models.user_email import UserEmail
        user_email = UserEmail.select().where(
            (UserEmail.email == field.data) &
            ((UserEmail.activation_token_expires_at >= datetime.utcnow()) |
             (UserEmail.activation_state == 'active'))).first()
        if user_email:
            raise ValidationError('Email address is already registered')

    def validate_username(self, field):
        """Validates username existing."""
        from ...models.user import User
        user = User.select().where(
            User.username == field.data).first()
        if user:
            raise ValidationError('This username is already taken')


def build_signup_form(request):
    return build_form(SignupForm, request)
