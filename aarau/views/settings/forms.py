from wtforms import (
    StringField,
    PasswordField,
    HiddenField,
    SubmitField,
)
from wtforms import ValidationError, validators as v

from ..forms import PASSWORD_PATTERN
from ..forms import SecureForm, FailureForm, build_form


class ChangePasswordForm(SecureForm):
    """
    """
    current_password = PasswordField('Current password', [
        v.Required(),
        v.Length(min=6, max=32),
    ])
    new_password = PasswordField('New password', [
        v.Required(),
        v.Regexp(PASSWORD_PATTERN),
        v.Length(min=6, max=32),
    ])
    new_password_confirmation = PasswordField('Password confirmation', [
        v.Required(),
        v.EqualTo('new_password', message='Passwords must match'),
    ])
    submit = SubmitField('Change')


def change_password_form_factory(request, user):
    class AChangePasswordForm(ChangePasswordForm):
        def validate_new_password(self, field):
            if user.password == user.__class__.encrypt_password(field.data):
                raise ValidationError(
                    'New password is same as current password')
    return build_form(AChangePasswordForm, request)


class NewEmailForm(SecureForm):
    """
    """
    new_email = StringField('New Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])
    submit = SubmitField('Add')

    def validate_new_email(self, field):
        raise NotImplementedError


def new_email_form_factory(request):
    class ANewEmailForm(NewEmailForm):
        def validate_new_email(self, field):
            from ...models.user_email import UserEmail
            user_email = UserEmail.select().where(
                UserEmail.email == field.data).first()
            if user_email:
                raise ValidationError('Email is already registered.')
    return build_form(ANewEmailForm, request)


class DeleteEmailForm(SecureForm):
    """
    """
    email = HiddenField('Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])

    def validate_email(self, field):
        raise NotImplementedError


def delete_email_form_factory(request, user_email):
    if not user_email or user_email.type == 'primary':
        return build_form(FailureForm, request)

    class ADeleteEmailForm(DeleteEmailForm):
        def validate_email(self, field):
            if not user_email:
                raise ValidationError()
    return build_form(ADeleteEmailForm, request)


class ChangeEmailForm(SecureForm):
    """
    """
    email = HiddenField('Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])

    def validate_email(self, field):
        raise NotImplementedError


def change_email_form_factory(request, user_email):
    if not user_email or user_email.activation_state == 'pending' or \
       user_email.type == 'primary':
            return build_form(FailureForm, request)

    class AChangeEmailForm(ChangeEmailForm):
        def validate_email(self, field):
            if not user_email:
                raise ValidationError()

    return build_form(AChangeEmailForm, request)
