from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms import validators as v

from aarau.views.form import SecureForm, build_form


class ResetPasswordRequestForm(SecureForm):
    """
    """
    email = StringField('Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])
    submit = SubmitField('Request')


def reset_password_request_form_factory(request):
    class AResetPasswordRequestForm(ResetPasswordRequestForm):
        pass

    return build_form(AResetPasswordRequestForm, request)


class ResetPasswordForm(SecureForm):
    """
    """
    new_password = PasswordField('New password', [
        v.Required(),
        v.Regexp(
            '(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])'
            '(?=.*[A-z0-9\-\_\+\=\$\%\#\&\!\?])'),
        v.Length(min=6, max=32),
    ])
    new_password_confirmation = PasswordField('Password confirmation', [
        v.Required(),
        v.EqualTo('new_password', message='Passwords must match'),
    ])

    submit = SubmitField('Request')


def reset_password_form_factory(request):
    class AResetPasswordForm(ResetPasswordForm):
        pass

    return build_form(AResetPasswordForm, request)
