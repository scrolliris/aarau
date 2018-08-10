from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms import validators as v

from aarau.views.form import SecureForm, build_form


class ResetPasswordRequestFormBase(SecureForm):
    email = StringField('Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])
    submit = SubmitField('Request')


class ResetPasswordRequestForm(ResetPasswordRequestFormBase):
    pass


def build_reset_password_request_form(request):
    return build_form(ResetPasswordRequestForm, request)


class ResetPasswordFormBase(SecureForm):
    new_password = PasswordField('New password', [
        v.Required(),
        v.Regexp(
            r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])'
            r'(?=.*[A-Za-z0-9\-\_\+\=\$\%\#\&\!\?])'),
        v.Length(min=6, max=32),
    ])
    new_password_confirmation = PasswordField('Password confirmation', [
        v.Required(),
        v.EqualTo('new_password', message='Passwords must match'),
    ])

    submit = SubmitField('Request')


class ResetPasswordForm(ResetPasswordFormBase):
    pass


def build_reset_password_form(request):
    return build_form(ResetPasswordForm, request)
